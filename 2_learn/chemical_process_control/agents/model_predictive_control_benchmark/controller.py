import copy
import math
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from composabl import SkillController
from gekko import GEKKO
from scipy import interpolate
from scipy.integrate import odeint

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"

class MPCController(SkillController):
    def __init__(self, *args, **kwargs):
        self.count = 0
        # create metrics db
        try:
            self.df = pd.read_pickle(f"{PATH_HISTORY}/history.pkl")
            if self.metrics == 'fast':
                self.plot_metrics()
        except:
            self.df = pd.DataFrame()

        #initialize variables
        self.display_mpc_vals = False
        remote_server = True # use a remote server to process calculations

        # Steady State Initial Condition
        u_ss = 280.0
        # Tf = Feed Temperature (K)
        Tf = 298.2 #K
        # Caf = Feed Concentration (kmol/m^3)
        Caf = 10 #kmol/m3

        # Steady State as initial condition for the states
        Ca_ss = 8.5698
        T_ss = 311.2612
        self.x0 = np.empty(2)
        self.x0[0] = Ca_ss
        self.x0[1] = T_ss

        # GEKKO linear MPC
        self.m = GEKKO(remote=remote_server)

        self.m.time = np.linspace(0, 90, num=90) #simulate 45 minutes (0.5 minute per controller action)

        # initial conditions
        Tc0 = 292
        T0 = 311
        Ca0 = 8.57

        tau = self.m.Const(value = 3) #3
        Kp = self.m.Const(value = 0.65) #0.75

        # Manipulated and Controlled Variables
        self.m.Tc = self.m.MV(value = Tc0,lb=273,ub=322) #mv with constraints
        self.m.T = self.m.CV(value = T_ss) #cv

        # Process dynamic model
        self.m.Equation(tau * self.m.T.dt() == -(self.m.T - T0) + Kp * (self.m.Tc - Tc0))

        #MV tuning - Cooling Temp
        self.m.Tc.STATUS = 1
        self.m.Tc.FSTATUS = 0
        self.m.Tc.DMAXHI = 10   # constrain movement up
        self.m.Tc.DMAXLO = -10  # quick action down

        #CV tuning - Tr Reactor Temp
        self.m.T.STATUS = 1
        self.m.T.FSTATUS = 1
        self.m.T.SP = 311
        #m.T.UPPER = 400 #Upper constraint
        self.m.T.TR_INIT = 2
        self.m.T.TAU = 1.0 # time constant of trajectory

        self.m.options.CV_TYPE = 2 # the objective is an l2-norm (squared error)
        self.m.options.IMODE = 6 # MPC
        self.m.options.SOLVER = 3

        # time Interval (min)
        time = 90 #simulation time (min)
        self.t = np.linspace(0,time, time)

        # Store results for plotting
        self.Ca = np.ones(len(self.t)) * Ca_ss
        self.T = np.ones(len(self.t)) * T_ss
        #Tsp = np.ones(len(t)) * T_ss
        Tsp = []
        Csp = []
        self.u = np.ones(len(self.t)) * u_ss

        # Set points - reference
        p1 = 22 #time to start the transition
        p2 = 74 #time to finish the transition

        T_ = interpolate.interp1d([0,p1,p2,time,time+1], [311.2612,311.2612,373.1311,373.1311,373.1311])
        C = interpolate.interp1d([0,p1,p2,time, time+1], [8.57,8.57,2,2,2])

    async def compute_action(self, obs, action):
        #self.T, self.Tc, self.Ca, self.Cref, self.Tref

        df = pd.DataFrame()
        t = self.t
        i = self.count
        noise = 0

        # simulate one time period
        ts = [t[i],t[i+1]]
        # retrieve measurements
        # apply noise
        σ_max1 = noise * (8.5698 - 2)
        σ_max2 = noise * ( 373.1311 - 311.2612)
        σ_Ca = random.uniform(-σ_max1, σ_max1)
        σ_T = random.uniform(-σ_max2, σ_max2)
        obs['T'] = obs['T'] + σ_T
        obs['Ca']  = obs['Ca'] + σ_Ca

        # insert measurement
        self.m.T.MEAS = obs['T']
        # update setpoint
        self.m.T.SP = obs['Tref']
        Tref = obs['Tref']
        Cref = obs['Cref']
        # solve MPC
        self.m.solve(disp=self.display_mpc_vals)
        # change to a fixed starting point for trajectory
        self.m.T.TR_INIT = 2
        # retrieve new Tc values
        self.u[i+1] = self.m.Tc.NEWVAL
        newTc = self.m.Tc.NEWVAL
        # update initial conditions
        newCa = self.Ca[i+1]
        newT = self.T[i+1]
        self.x0[0] = self.Ca[i+1]
        self.x0[1] = self.T[i+1]

        error = (self.x0[0] - Cref)**2
        error = (self.x0[1] - Tref)**2

        #generate dataframe
        df_t = pd.DataFrame([[i,self.Ca[i+1],self.T[i+1],newTc, Tref,Cref ]], columns = ['time','Ca','T','Tc','Tref','Cref'])
        self.df = pd.concat([self.df, df_t])
        #self.df.to_pickle("./cstr/linear_mpc/history.pkl")

        self.count += 1
        dTc = float(newTc) - float(obs['Tc'])
        return [dTc]

    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False
