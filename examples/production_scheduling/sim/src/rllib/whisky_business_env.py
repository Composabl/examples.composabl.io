import math
import os
import random
import numpy as np
import simpy
import gymnasium as gym
from gymnasium.spaces import Box, Discrete

from simulation.recipe import RecipeNames
from rllib.ray_controller import RLLibController

class WhiskeyBusinessEnv(gym.Env):    
    def default_reward_fn(self, step_state,cookie_price,cupcake_price,cake_price):
        reward = 0
        if (step_state['completed_cookies'] > 0):
            reward += step_state['completed_cookies']*3 
        if (step_state['completed_cupcakes'] > 0):
            reward += step_state['completed_cupcakes']*3
        if (step_state['completed_cake'] > 0):
            reward += step_state['completed_cake']*12
        return reward
    
    def __init__(self, env_config):
        if "debug" in env_config["env_config"]:
            debug = env_config["env_config"]["debug"]
        else:
            debug = False

        if "reward_fn" in env_config["env_config"]:
            self.reward_fn = env_config["env_config"]["reward_fn"]
        else:
            self.reward_fn = self.default_reward_fn

        if "cookies_price" in env_config["env_config"]:
            self.cookies_price = env_config["env_config"]["cookies_price"]
        else:
            self.cookies_price = 0

        if "cupcake_price" in env_config["env_config"]:
            self.cupcake_price = env_config["env_config"]["cupcake_price"]
        else:
            self.cupcake_price = 0

        if "cake_price" in env_config["env_config"]:
            self.cake_price = env_config["env_config"]["cake_price"]
        else:
            self.cake_price = 0

        if "cookies_demand" in env_config["env_config"]:
            self.cookies_demand = env_config["env_config"]["cookies_demand"]
        else:
            self.cookies_demand = 0

        if "cupcake_demand" in env_config["env_config"]:
            self.cupcake_demand = env_config["env_config"]["cupcake_demand"]
        else:
            self.cupcake_demand = 0

        if "cake_demand" in env_config["env_config"]:
            self.cake_demand = env_config["env_config"]["cake_demand"]
        else:
            self.cake_demand = 0
        
        if "cookies_cost" in env_config["env_config"]:
            self.cookies_cost = env_config["env_config"]["cookies_cost"]
        else:
            self.cookies_cost = 0

        if "cupcake_cost" in env_config["env_config"]:
            self.cupcake_cost = env_config["env_config"]["cupcake_cost"]
        else:
            self.cupcake_cost = 0

        if "cake_cost" in env_config["env_config"]:
            self.cake_cost = env_config["env_config"]["cake_cost"]
        else:
            self.cake_cost = 0

        env = simpy.Environment()
        self.controller = RLLibController(env,debug)
        max_avail_actions = len(self.step_action_dict)
        self.action_space = Discrete(max_avail_actions)


        self.observation_space = gym.spaces.Dict({
            "action_mask":  Box(0, 1, shape=(max_avail_actions, ),dtype=np.bool_),
            "observations":  Box(0, 500, shape=(len(self.default_state)-3, ),dtype=float),
            "dessert_cases":  Box(0, 700, shape=(3, ),dtype=float),
            "dessert_prices":  Box(0, 50, shape=(3, ),dtype=float),
            "dessert_demand":  Box(0, 100, shape=(3, ),dtype=float),
            "dessert_cost":  Box(0, 100, shape=(3, ),dtype=float),
        })

    step_action_dict = {
            0:"wait",
            1:"Chip_mix_cookies",
            2:"Chip_mix_cupcakes",
            3:"Chip_mix_cakes",
            4:"Coco_mix_cookies",
            5:"Coco_mix_cupcakes",
            6:"Coco_mix_cakes",
            7:"Eclair_mix_cookies",
            8:"Eclair_mix_cupcakes",
            9:"Eclair_mix_cakes",
            10:"Chip_bake_from_Mixer_1",
            11:"Chip_bake_from_Mixer_2",
            12:"Coco_bake_from_Mixer_1",
            13:"Coco_bake_from_Mixer_2",
            14:"Eclair_bake_from_Mixer_1",
            15:"Eclair_bake_from_Mixer_2",
            16:"Chip_decorate_from_Oven_1",
            17:"Chip_decorate_from_Oven_2",
            18:"Chip_decorate_from_Oven_3",
            19:"Eclair_decorate_from_Oven_1",
            20:"Eclair_decorate_from_Oven_2",
            21:"Eclair_decorate_from_Oven_3",
            22:"Reese_decorate_from_Oven_1",
            23:"Reese_decorate_from_Oven_2",
            24:"Reese_decorate_from_Oven_3"
        }
    
    default_state = {
        'sim_time' : 480,
        'baker_1_time_remaining' : 0,
        'baker_2_time_remaining' : 0,
        'baker_3_time_remaining' : 0,
        'baker_4_time_remaining' : 0,

        # EQUIPMENT
        'mixer_1_recipe' : RecipeNames(0).value,
        'mixer_1_time_remaining' : 0,
        'mixer_2_recipe' : RecipeNames(0).value,
        'mixer_2_time_remaining' : 0,

        'oven_1_recipe' : RecipeNames(0).value,
        'oven_1_time_remaining' : 0,
        'oven_2_recipe' : RecipeNames(0).value,
        'oven_2_time_remaining' : 0,
        'oven_3_recipe' : RecipeNames(0).value,
        'oven_3_time_remaining' : 0,

        'decorating_station_1_recipe' : RecipeNames(0).value,
        'decorating_station_1_time_remaining' : 0,
        'decorating_station_2_recipe' : RecipeNames(0).value,
        'decorating_station_2_time_remaining' : 0,

        # DESSERT CASE
        'completed_cookies' : 0,
        'completed_cupcakes' : 0,
        'completed_cake' : 0,
    }
    
    current_state = default_state
    
    def set_reward_fn(self,reward_fn):
        self.reward_fn = reward_fn

    def build_observation_space(self, bakery_state): 

        dessert_cases = {}
        dessert_cases['cookies'] = bakery_state['completed_cookies']
        dessert_cases['cupcakes'] = bakery_state['completed_cupcakes']
        dessert_cases['cakes'] = bakery_state['completed_cake']

        strip_bakery_state_int = list(bakery_state.values())

        del strip_bakery_state_int[21]
        del strip_bakery_state_int[20]
        del strip_bakery_state_int[19]
        
        strip_bakery_state_float = [float(x) for x in strip_bakery_state_int]
        

        self.dessert_cases_list = list(dessert_cases.values())

        return {
            "action_mask":  np.array(self.controller.get_mask(), dtype=np.bool_), 
            "observations":  np.array(strip_bakery_state_float, dtype=float),
            "dessert_cases": np.array(self.dessert_cases_list, dtype=float),
            "dessert_prices": np.array([self.cookies_price, self.cupcake_price, self.cake_price], dtype=float),
            "dessert_demand": np.array([self.cookies_demand, self.cupcake_demand, self.cake_demand], dtype=float),
            "dessert_cost": np.array([self.cookies_cost, self.cupcake_cost, self.cake_cost], dtype=float)
        }

    def reset(self, *, seed=None, options=None):
        reset_state = self.controller.reset(self.default_state)
        return self.build_observation_space(reset_state), {}
    
    def step(self, action):
        if self.controller.get_mask()[action] == 0 :
            action = 0

        self.current_state = self.controller.step(action)

        reward = self.reward_fn(self.current_state,self.cookies_price,self.cupcake_price,self.cake_price)
        
        terminate = self.current_state['sim_time'] <= 0

        return self.build_observation_space(self.current_state), reward, terminate, False, {}
