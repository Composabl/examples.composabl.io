import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController
from gekko import GEKKO


class OrderController():
    def __init__(self):
        self.count = 0
        self.action_count = 1

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

        self.display_mpc_vals = False
        # solve
        self.m.solve(disp=self.display_mpc_vals)

        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True

    def reset(self):
        self.count = 0
        self.action_count = 1

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

        self.display_mpc_vals = False
        # solve
        self.m.solve(disp=self.display_mpc_vals)

        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True

    def compute_action(self, obs):
        action = 0 # wait
        self.count += 1


        x1 = [int(x) for x in self.u1.value]
        x2 = [int(x) for x in self.u2.value]
        x3 = [int(x) for x in self.u3.value]
        self.x1 = x1

        wt = [int(x) for x in self.wt.value]

        if self.action_count >= len(wt):
            return action

        wt_plan = wt[self.action_count]

        if self.count < wt_plan:

            if self.make_cake:
                if x3[self.action_count] == 1:
                    #print('Produce Cake')
                    action = MakeCakeController().compute_action(obs)
                    #action = [2]
                    self.make_cake = False
                    self.make_cupcake = True
                    self.make_cookie = True
                    return action

            if self.make_cupcake:
                if x2[self.action_count] == 1:
                    #print('Produce Cupcake')
                    action = MakeCupcakeController().compute_action(obs)
                    #action = [1]
                    self.make_cake = True
                    self.make_cupcake = False
                    self.make_cookie = True
                    return action

            if self.make_cookie:
                if x1[self.action_count] == 1:
                    #print('Produce Cookie')
                    action = MakeCookieController().compute_action(obs)
                    #action = [0]
                    self.make_cake = True
                    self.make_cupcake = True
                    self.make_cookie = False
                    return action


        else:
            self.action_count += 1

        return action

    def compute_termination(self, transformed_obs, action):
        if self.action_count > len(self.x1):
            return True
        else:
            return False

#cont = OrderController()

#for i in range(480):
#    print(cont.compute_action(obs=[1,1,1]))
