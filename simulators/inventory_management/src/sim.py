import math
import random
import numpy as np
import simpy as sp
import matplotlib.pyplot as plt

from composabl_core.agent.scenario import Scenario
import gymnasium as gym


class Env(gym.Env):
    def __init__(self):
        '''
        actions = 2 :
        observation_variables = 9 :
        run_time: time in days to run the simulation (simpy)
        '''
        obs_space = {"inventory": {"low": 0, "high": 1e10},
                     "balance": {"low": -200, "high": 1e10},
                     "num_ordered": {"low": 0, "high": 1000.0},
                     "holding_cost": {"low": 0, "high": 1000.0},
                     "cost_price": {"low": 0, "high": 1e10},
                     "delay_days_until_delivery": {"low": 0, "high": 1000.0},
                     "customer_demand_min": {"low": 1, "high": 1000.0},
                     "customer_demand_max": {"low": 1, "high": 1000.0},
                     "selling_price": {"low": 0, "high": 1e4}
                    }

        low_list = [x['low'] for x in obs_space.values()]
        high_list = [x['high'] for x in obs_space.values()]

        self.observation_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        action_space = {"order_cutoff": {"low": 0, "high": 100},
                        "order_target": {"low": 0, "high": 100},
                        }

        low_act_list = [x['low'] for x in action_space.values()]
        high_act_list = [x['high'] for x in action_space.values()]

        self.action_space = gym.spaces.Box(low=np.array(low_act_list), high=np.array(high_act_list))

        self.scenario: Scenario = None

        self.order_cutoff = 10
        self.order_target = 30
        self.holding_cost = 2
        self.selling_price = 100
        self.cost_price = 50
        self.delay_days_until_delivery = 2
        self.customer_demand_min = 1
        self.customer_demand_max = 4
        self.run_time = 30

        self.obs_time = []
        self.inventory_level = []
        self.balance_history = []
        self.num_ordered_list = []
        self.scenario = None

    def handle_order(self, env, order_target, cost_price=50, delay_days_until_delivery=2):
        global inventory, balance, num_ordered

        num_ordered = order_target - inventory
        #print(f'{env.now} place order for  {num_ordered}')
        balance -= cost_price * num_ordered
        yield env.timeout(delay_days_until_delivery)
        inventory += num_ordered
        num_ordered = 0
        #print(f'{env.now} received order, {inventory} in inventory')

    def generate_interarrival(self):
        return np.random.exponential(1 / 5)

    def generate_demand(self, customer_demand_min=1, customer_demand_max=4):
        return np.random.randint(customer_demand_min, customer_demand_max)

    def warehouse_run(self, env,
                      order_cutoff,
                      order_target,
                      holding_cost=2,
                      selling_price=100,
                      cost_price=50,
                      delay_days_until_delivery=2,
                      customer_demand_min=1,
                      customer_demand_max=4):

        global inventory, balance, num_ordered

        inventory = order_target
        balance = 0
        num_ordered = 0

        while True:
            interarrival = self.generate_interarrival()
            yield env.timeout(interarrival)
            balance -= inventory * holding_cost * interarrival
            demand = self.generate_demand(customer_demand_min, customer_demand_max)

            if demand < inventory:
                balance += selling_price * demand
                inventory -= demand
                #print(f'{env.now} Sold {demand}')
            else:
                balance += selling_price * inventory
                inventory = 0
                #print(f'{env.now} Sold {inventory} (out of stock)')

            if inventory < order_cutoff and num_ordered == 0:
                env.process(self.handle_order(env, order_target, cost_price, delay_days_until_delivery))

    def observe_values(self, env):
        global inventory, balance, num_ordered

        while True:
            self.obs_time.append(env.now)
            self.inventory_level.append(inventory)
            self.balance_history.append(balance)
            self.num_ordered_list.append(num_ordered)
            obs_dt = 0.1
            yield env.timeout(obs_dt)

    def reset(self):
        # Define scenario in the simulation
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])
        else:
            self.order_cutoff = 10
            self.order_target = 30
            self.holding_cost = 2
            self.selling_price = 100
            self.cost_price = 50
            self.delay_days_until_delivery = 2
            self.customer_demand_min = 1
            self.customer_demand_max = 4
            self.run_time = 30


        # time counter
        self.cnt = 0

        self.y_list = []
        self.error_list = []

        self.obs = {"inventory": 0,
                    "balance": 0,
                    "num_ordered": 0,
                    "holding_cost": float(self.holding_cost),
                    "cost_price": float(self.cost_price),
                    "delay_days_until_delivery": float(self.delay_days_until_delivery),
                    "customer_demand_min": float(self.customer_demand_min),
                    "customer_demand_max": float(self.customer_demand_max),
                    "selling_price": float(self.selling_price)
                    }
        print("RESET", self.obs)
        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        print("Step: ", num_ordered_total, self.balance_history)
        simpyenv = sp.Environment()

        simpyenv.process(self.warehouse_run(
            env=simpyenv,
            order_cutoff=action[0],
            order_target=action[1],
            holding_cost=self.holding_cost,
            selling_price=self.selling_price,
            cost_price=self.cost_price,
            delay_days_until_delivery=self.delay_days_until_delivery,
            customer_demand_min=self.customer_demand_min,
            customer_demand_max=self.customer_demand_max
        ))

        simpyenv.process(self.observe_values(simpyenv))
        simpyenv.run(until=self.run_time)

        num_ordered_total = sum(self.num_ordered_list)
        print("Step: ", num_ordered_total, self.balance_history)

        #TODO: new features
        # order max, order mean, balance total, balance mean, balance min,
        # inventory max, inventory min, inventory mean, inventory std
        # times ordered

        # Increase time counter
        self.cnt += 1

        #REWARD
        reward = 0

        done = False

        # Constraints to break the simulation
        if self.cnt == self.run_time:
            done = True

        self.obs = {"inventory": self.inventory_level[-1],
                    "balance": self.balance_history[-1],
                    "num_ordered": num_ordered_total,
                    "holding_cost": self.holding_cost,
                    "cost_price": self.cost_price,
                    "delay_days_until_delivery": self.delay_days_until_delivery,
                    "customer_demand_min": self.customer_demand_min,
                    "customer_demand_max": self.customer_demand_max,
                    "selling_price": self.selling_price
                    }

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, reward, done, False, info

    def render(self, mode='human', close=False):
        plt.plot(self.obs_time, self.inventory_level)
        plt.xlabel("Simulation time (days)")
        plt.ylabel("Inventory level")
        plt.show()

        plt.plot(self.obs_time, self.balance_history)
        plt.xlabel("Simulation time (days)")
        plt.ylabel("Balance History ($)")
        plt.show()

        plt.plot(self.obs_time, self.num_ordered_list)
        plt.xlabel("Simulation time (days)")
        plt.ylabel("Order History")
        plt.show()


