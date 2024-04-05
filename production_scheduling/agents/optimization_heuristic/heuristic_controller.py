import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController
from gekko import GEKKO
from sensors import sensors

class OrderController():
    def __init__(self):
        self.count = 0
        self.action_count = 1

        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True

    def compute_action(self, obs):
        print('COMPUTE')
        old_obs = obs.copy()
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))

        action = 0 # wait
        self.count += 1
        x1 = 0
        x2 = 0
        x3 = 0

        dem_cake = obs['cake_demand']
        dem_cupcake = obs['cupcake_demand']
        dem_cookie = obs['cookies_demand']

        if (obs['completed_cake'] >= dem_cake) and (obs['completed_cupcakes'] >= dem_cupcake) and (obs['completed_cookies'] >= dem_cookie):
            print("COMPLETED")
            return action

        if obs['completed_cake'] < dem_cake:
            x3 = 1

        if obs['completed_cupcakes'] < dem_cupcake:
            x2 = 1

        if (obs['completed_cookies'] < dem_cookie) and (x3 + x2 < 2):
            self.make_cookie = True
            x1 = 1

        if self.make_cake:
            if x3 == 1:
                print('Produce Cake')
                action = MakeCakeController().compute_action(old_obs)
                #action = [2]
                self.make_cake = False
                self.make_cupcake = True
                self.make_cookie = True
                return action

        if self.make_cupcake:
            if x2 == 1:
                print('Produce Cupcake')
                action = MakeCupcakeController().compute_action(old_obs)
                #action = [1]
                self.make_cake = True
                self.make_cupcake = False
                self.make_cookie = True
                return action

        if self.make_cookie:
            if x1 == 1:
                print('Produce Cookie')
                action = MakeCookieController().compute_action(old_obs)
                #action = [0]
                self.make_cake = True
                self.make_cupcake = True
                self.make_cookie = False
                return action

        return action


    def compute_termination(self, transformed_obs, action):
        return False
