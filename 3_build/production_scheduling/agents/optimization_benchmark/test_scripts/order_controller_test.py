from composabl import Controller

import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO
from sensors import sensors


class OrderController(Controller):
    def __init__(self):
        self.total_time = 0 

        # Two products at a time
        self.m = GEKKO(remote=False)
        nt = 10
        #m.time = np.linspace(0,nt,2)
        self.m.time = [i for i in range(0,nt)]

        #variables
        self.u1 = self.m.MV(value=0, lb=0, ub=1, integer=True) #input
        self.u2 = self.m.MV(value=0, lb=0, ub=1, integer=True) #input
        self.u3 = self.m.MV(value=0, lb=0, ub=1, integer=True) #input

        # Variables
        q = self.m.SV(value=0, lb=0, integer=True) #state variable
        self.wt = self.m.SV(value=0, lb=0, ub=480, integer=True)
        r = self.m.SV(value=0, lb=0, ub=5000, integer=True)

        ## CONSTRAINTS
        # STATUS = 0, optimizer doesn't adjust value;  STATUS = 1, optimizer can adjust
        self.u1.STATUS = 1
        self.u2.STATUS = 1
        self.u3.STATUS = 1

        prices = {
            1: 5,
            2: 7,
            3: 10
        }

        quantities = {
            1: 12,
            2: 6,
            3: 1
        }

        # Equations
        self.m.Equations([q.dt() == 12*self.u1 + 6*self.u2 + 1*self.u3,
                    self.wt.dt() == self.m.max2(self.m.max2(28*self.u1,57*self.u2),80*self.u3),
                    self.wt <= 480,
                    r.dt() == 12*5*self.u1 + 6*7*self.u2 + 1*10*self.u3,
                    self.u1 + self.u2 + self.u3 <= 2
                    ])


        self.m.Maximize(r) # Objective function

        self.m.options.IMODE = 6 # optimal control mode

        
    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
    
    def compute_action(self, obs):
        self.total_time += 1

        self.display_mpc_vals = False
        # solve 
        self.m.solve(disp=self.display_mpc_vals)

        x1 = [int(x) for x in self.u1.value]
        x2 = [int(x) for x in self.u2.value]
        x3 = [int(x) for x in self.u3.value]

        wt = [int(x) for x in self.wt.value]

        #convert into [0,1,2]

        return [x1, x2, x3, wt]
    
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False
    