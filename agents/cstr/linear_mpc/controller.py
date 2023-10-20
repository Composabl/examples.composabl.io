from composabl import Controller

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from gekko import GEKKO
from scipy import interpolate
import math
import random
import pandas as pd
import copy


class MPCController(Controller):
    def __init__(self):
        self.count = 0
        # create metrics db
        try:
            self.df = pd.read_pickle('./cstr/linear_mpc/history.pkl')
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

        self.m.time = np.linspace(0, 45, num=90) #simulate 45 minutes (0.5 minute per controller action)

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
        time = 45 #simulation time (min)
        self.t = np.linspace(0,time, time)

        # Store results for plotting
        self.Ca = np.ones(len(self.t)) * Ca_ss
        self.T = np.ones(len(self.t)) * T_ss
        #Tsp = np.ones(len(t)) * T_ss
        Tsp = []
        Csp = []
        self.u = np.ones(len(self.t)) * u_ss

        # Set points - reference
        p1 = 10 #time to start the transition
        p2 = 36 #time to finish the transition

        T_ = interpolate.interp1d([0,p1,p2,time,time+1], [311.2612,311.2612,373.1311,373.1311,373.1311])
        C = interpolate.interp1d([0,p1,p2,time, time+1], [8.57,8.57,2,2,2])
        
    def compute_action(self, obs):
        #print(obs) #self.T, self.Tc, self.Ca, self.Cref, self.Tref
        obs_org = copy.deepcopy(obs)
        #if type(obs)
        obs = {
            'T': obs[0],
            'Tc': obs[1],
            'Ca': obs[2],
            'Cref': obs[3],
            'Tref': obs[4]
        }
        
        df = pd.DataFrame()
        t = self.t
        i = self.count
        noise = 0

        # simulate one time period
        ts = [t[i],t[i+1]]
        ###y = odeint(cstr,x0,ts,args=(u[i],Tf,Caf))
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
        ###Tsp.append(Tref)
        ###Csp.append(Cref)
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
        #Ca_error.append(error)
        error = (self.x0[1] - Tref)**2
        #Tref_error.append(error)

        #generate dataframe
        df_t = pd.DataFrame([[i,self.Ca[i+1],self.T[i+1],Tref,Cref ]], columns = ['time','Ca','T','Tref','Cref'])
        self.df = pd.concat([self.df, df_t])
        self.df.to_pickle("./cstr/linear_mpc/history.pkl") 

        #print('CA', newTc, obs['Tc']) 

        self.count += 1
        dTc = float(newTc) - float(obs['Tc'])
        #dTc = 0
        #obs = obs_org
        return [dTc]

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']
    
    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False
    



"""#simulation config
sim_max = 1 # number of simulations
noise = 0.00 # error pct
graphics = True # live graphics 


# Create plot
if graphics == True:
    plt.figure(figsize=(10,7))
    plt.ion()
    plt.show()

df_train = pd.DataFrame()
# Simulate CSTR with controller
for i in range(len(t)-1):
    # simulate one time period
    ts = [t[i],t[i+1]]
    y = odeint(cstr,x0,ts,args=(u[i],Tf,Caf))
    # retrieve measurements
    # apply noise
    σ_max1 = noise * (8.5698 - 2)
    σ_max2 = noise * ( 373.1311 - 311.2612)
    σ_Ca = random.uniform(-σ_max1, σ_max1)
    σ_T = random.uniform(-σ_max2, σ_max2)
    Ca[i+1] = y[-1][0] + σ_T
    T[i+1] = y[-1][1] + σ_Ca
    # insert measurement
    m.T.MEAS = T[i+1]
    # update setpoint
    m.T.SP = T_(i+1)
    Tref = T_(i+1)
    Cref = C(i+1)
    Tsp.append(Tref)
    Csp.append(Cref)
    # solve MPC
    m.solve(disp=display_mpc_vals)
    # change to a fixed starting point for trajectory
    m.T.TR_INIT = 2
    # retrieve new Tc values
    u[i+1] = m.Tc.NEWVAL
    # update initial conditions
    x0[0] = Ca[i+1]
    x0[1] = T[i+1]

    error = (x0[0] - Cref)**2
    Ca_error.append(error)
    error = (x0[1] - Tref)**2
    Tref_error.append(error)

    #generate dataframe
    df_t = pd.DataFrame([[i,Ca[i+1],T[i+1],Tref,Cref ]], columns = ['sim_time','Ca','T','Tref','Cref'])
    df_train = df_train.append(df_t)


    # Plot the results
    if graphics == True:
        plt.clf()
        
        plt.subplot(3,1,1)
        plt.plot(t[0:i],u[0:i],'k.-',lw=2)
        plt.ylabel('Cooling Tc (K)')
        plt.legend(['Jacket Temperature'],loc='best')

        plt.subplot(3,1,2)
        plt.plot(t[0:i],Ca[0:i],'b.-',lw=3)
        plt.plot(t[0:i],Csp[0:i],'k--',lw=2,label=r'$C_{sp}$')
        plt.ylabel('Ca (mol/L)')
        plt.legend(['Reactor Concentration','Concentration Setpoint'],loc='best')

        plt.subplot(3,1,3)
        plt.plot(t[0:i],Tsp[0:i],'k--',lw=2,label=r'$T_{sp}$')
        plt.plot(t[0:i],T[0:i],'b.-',lw=3,label=r'$T_{meas}$')
        plt.plot(t[0:i],[400 for x in range(0,i)],'r--',lw=1)
        plt.ylabel('T (K)')
        plt.xlabel('Time (min)')
        plt.legend(['Temperature Setpoint','Reactor Temperature'],loc='best')
        plt.draw()
        plt.pause(0.001)

    Tr_out.append(Tr_out_id)
    Cr_out.append(Cr_out_id)
    Tr_list_.append(list(T))
    Cr_list_.append(list(Ca))
    #plt.close()
    #Metrics
    df_train = df_train.reset_index()
    print(df_train)
    #SS1
    Ca_RMS = math.sqrt(np.average(list(df_train.loc[:'9','Ca'] - df_train.loc[:'9','Cref']))**2 )
    Tref_RMS = math.sqrt(np.average(list(df_train.loc[:'9','T'] - df_train.loc[:'9','Tref']))**2 )
    print('SS1: ',Ca_RMS, Tref_RMS)
    #print(df_train.iloc[:23,:]) # SS1
    #print(df_train.iloc[24:75,8:]) # Trans
    Ca_RMS = math.sqrt(np.average(list(df_train.loc['10':'34','Ca'] - df_train.loc['10':'34','Cref']))**2 )
    Tref_RMS = math.sqrt(np.average(list(df_train.loc['10':'34','T'] - df_train.loc['10':'34','Tref']))**2 )
    print('Trans:' , Ca_RMS, Tref_RMS)
    #print(df_train.iloc[76:,:]) # SS2
    Ca_RMS = math.sqrt(np.average(list(df_train.loc['35':,'Ca'] - df_train.loc['35':,'Cref']))**2 )
    Tref_RMS = math.sqrt(np.average(list(df_train.loc['35':,'T'] - df_train.loc['35':,'Tref']))**2 )
    print('SS2:' , Ca_RMS, Tref_RMS)

    #df_train.to_csv('cstr_simulator_data.csv', index=False)
    Ca_RMS = math.sqrt(np.average(list(df_train.loc[7:'13','Ca'] - df_train.loc[7:'13','Cref']))**2 )
    print(df_train.loc['7':'13','Ca'])
    Tref_RMS = math.sqrt(np.average(list(df_train.loc[7:'13','T'] - df_train.loc[7:'13','Tref']))**2 )
    print('Bound 1: ',Ca_RMS, Tref_RMS)

    Ca_RMS = math.sqrt(np.average(list(df_train.loc['32':'38','Ca'] - df_train.loc['32':'38','Cref']))**2 )
    Tref_RMS = math.sqrt(np.average(list(df_train.loc['32':'38','T'] - df_train.loc['32':'38','Tref']))**2 )
    print('Bound 2: ',Ca_RMS, Tref_RMS)

Ca_RMS = math.sqrt(np.average(Ca_error))
Tref_RMS = math.sqrt(np.average(Tref_error))

#print results
print("Ca RMS: ", Ca_RMS , "+- ", np.std(Ca_error))
print("Tr RMS: ", Tref_RMS, "+- ", np.std(Tref_error))
print("Thermal Runaway: ", (np.sum(Tr_out)/sim_max)*100 , " %")
print("Concentration Out: ", (np.sum(Cr_out)/sim_max)*100, " %" )

#plot multi run graph
Tref_list = Tsp
Cref_list = Csp
T_list = T
Ca_list = Ca
'''min_Tr = [min(np.array(Tr_list_)[:,i]) for i in range(iter_)]
max_Tr = [max(np.array(Tr_list_)[:,i]) for i in range(iter_)]
plt.fill_between([i/2 for i in range(len(T_list))] , min_Tr , max_Tr, alpha = 0.2)
plt.plot([i/2 for i in range(len(Tref_list))],Tref_list,'k--',lw=2,label=r'$T_{sp}$')
plt.plot([i/2 for i in range(len(T_list))],[400 for x in range(len(T_list))],'r--',lw=1)
plt.title('Temperature')
plt.show()

min_Cr = [min(np.array(Cr_list_)[:,i]) for i in range(iter_)]
max_Cr = [max(np.array(Cr_list_)[:,i]) for i in range(iter_)]
plt.fill_between([i/2 for i in range(len(Ca_list))] , min_Cr , max_Cr, alpha = 0.2)
plt.plot([i/2 for i in range(len(Cref_list))],Cref_list,'k--',lw=2,label=r'$T_{sp}$')
plt.plot([i/2 for i in range(len(Ca_list))],[12 for x in range(len(T_list))],'r--',lw=1)
plt.plot([i/2 for i in range(len(Ca_list))],[0.1 for x in range(len(T_list))],'r--',lw=1)
plt.title('Concentration')
plt.show()'''

#generate dataframe
'''df_train = pd.read_csv(r'..\results-spec.csv')
df_t = pd.DataFrame()
df_t['date'] = [pd.to_datetime('now')]
df_t['model'] = ['linear_mpc']
df_t['runs'] = [sim_max]
df_t['noise'] = [noise]
df_t['CaRMS_mu'] = [Ca_RMS]
df_t['CaRMS_sigma'] = [np.std(Ca_error)]
df_t['TrRMS_mu'] = [Tref_RMS]
df_t['TrRMS_sigma'] = [np.std(Tref_error)]
df_t['runaway_pct'] = [(np.sum(Tr_out)/sim_max)]

df_train = df_train.append(df_t)

df_train.to_csv(r'..\results-spec.csv', index=False)'''"""
