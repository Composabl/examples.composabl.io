#from order_controller import OrderController
from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController
from gekko import GEKKO
from sensors import sensors

bake_scenarios = [
        {   # High Demand
            "cookies_demand": 100,
            "cupcake_demand": 18,
            "cake_demand": 5,
        },
        {   # Std Demand
            "cookies_demand": 60,
            "cupcake_demand": 18,
            "cake_demand": 2,
        },
        {   # Low Demand
            "cookies_demand": 20,
            "cupcake_demand": 6,
            "cake_demand": 1,
        },
        {   # Xmas Demand
            "cookies_demand": 260,
            "cupcake_demand": 10,
            "cake_demand": 1,
        },
        {   # Cupcake Wars
            "cookies_demand": 0,
            "cupcake_demand": 96,
            "cake_demand": 0,
        },
        {   # Cookie Wars
            "cookies_demand": 396,
            "cupcake_demand": 0,
            "cake_demand": 0,
        },
        {   # November Birthday
            "cookies_demand": 0,
            "cupcake_demand": 0,
            "cake_demand": 11,
        }
    ]

class OrderController():
    def __init__(self):
        self.count = 0 
        self.action_count = 1

        self.make_cake = True
        self.make_cupcake = True
        self.make_cookie = True
    
    def compute_action(self, obs):
        #print('COMPUTE')
        if type(obs) != dict:
            old_obs = obs.copy()
            sensors_name = [s.name for s in sensors]
            obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        else:
            if 'demand_predict' in list(obs.keys()):
                obs.pop('demand_predict')
            old_obs = obs
            for k, v in obs.items():
                obs[k] = float(v)

        action = 0 # wait
        self.count += 1
        x1 = 0
        x2 = 0
        x3 = 0
        
        dem_cake = obs['cake_demand']
        dem_cupcake = obs['cupcake_demand']
        dem_cookie = obs['cookies_demand']

        if (obs['completed_cake'] >= dem_cake) and (obs['completed_cupcakes'] >= dem_cupcake) and (obs['completed_cookies'] >= dem_cookie):
            #print("COMPLETED")
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
                #print('Produce Cake')
                action = MakeCakeController().compute_action(old_obs)
                #action = [2]
                self.make_cake = False
                self.make_cupcake = True
                self.make_cookie = True
                return action

        if self.make_cupcake:
            if x2 == 1:
                #print('Produce Cupcake')
                action = MakeCupcakeController().compute_action(old_obs)
                #action = [1]
                self.make_cake = True
                self.make_cupcake = False
                self.make_cookie = True
                return action

        if self.make_cookie:
            if x1 == 1:
                #print('Produce Cookie')
                action = MakeCookieController().compute_action(old_obs)
                #action = [0]
                self.make_cake = True
                self.make_cupcake = True
                self.make_cookie = False
                return action
            
        return action
        
    
    def compute_termination(self, transformed_obs, action):
        return False
    