from composabl import Controller

import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO
from sensors import sensors


class MakeCookieController(Controller):
    def __init__(self):
        self.total_time = 0 
        self.obs_history = []
 
    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
    
    def compute_action(self, obs):
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.total_time += 1

        #obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.obs_history.append(obs)
        
        action = 0 

        ## COOKIES
        # MIX
        if obs['baker_1_time_remaining'] == 0: #chip
            action = 1
        elif obs['baker_2_time_remaining'] == 0: #coco
            action = 4
        elif obs['baker_3_time_remaining'] == 0: #eclair
            action = 7

        # BAKE
        if obs['baker_1_time_remaining'] == 0: #chip
            if obs['mixer_1_recipe'] == 1:
                action = 10
            elif obs['mixer_2_recipe'] == 1:
                action = 11

        elif obs['baker_2_time_remaining'] == 0: #coco
            if obs['mixer_1_recipe'] == 1:
                action = 12
            elif obs['mixer_2_recipe'] == 1:
                action = 13
                
        elif obs['baker_3_time_remaining'] == 0: #eclair
            if obs['mixer_1_recipe'] == 1:
                action = 14
            elif obs['mixer_2_recipe'] == 1:
                action = 15

        # DECORATE
        if obs['baker_1_time_remaining'] == 0: #chip
            if obs['oven_1_recipe'] == 1:
                action = 16
            elif obs['oven_2_recipe'] == 1:
                action = 17
            elif obs['oven_3_recipe'] == 1:
                action = 18
                
        elif obs['baker_3_time_remaining'] == 0: #eclair
            if obs['oven_1_recipe'] == 1:
                action = 19
            elif obs['oven_2_recipe'] == 1:
                action = 20
            elif obs['oven_3_recipe'] == 1:
                action = 21

        elif obs['baker_4_time_remaining'] == 0: #reesee
            if obs['oven_1_recipe'] == 1:
                action = 22
            elif obs['oven_2_recipe'] == 1:
                action = 23
            elif obs['oven_3_recipe'] == 1:
                action = 24
        
        return action
    
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False


class MakeCupcakeController(Controller):
    def __init__(self):
        self.total_time = 0 
        self.obs_history = []
 
    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
    
    def compute_action(self, obs):
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.total_time += 1

        #obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.obs_history.append(obs)
        
        action = 0 

        ## CUPCAKES
        # MIX
        if obs['baker_1_time_remaining'] == 0: #chip
            action = 2
        elif obs['baker_2_time_remaining'] == 0: #coco
            action = 5
        elif obs['baker_3_time_remaining'] == 0: #eclair
            action = 8

        # BAKE
        if obs['baker_1_time_remaining'] == 0: #chip
            if obs['mixer_1_recipe'] == 2:
                action = 10
            elif obs['mixer_2_recipe'] == 2:
                action = 11

        elif obs['baker_2_time_remaining'] == 0: #coco
            if obs['mixer_1_recipe'] == 2:
                action = 12
            elif obs['mixer_2_recipe'] == 2:
                action = 13
                
        elif obs['baker_3_time_remaining'] == 0: #eclair
            if obs['mixer_1_recipe'] == 2:
                action = 14
            elif obs['mixer_2_recipe'] == 2:
                action = 15

        # DECORATE
        if obs['baker_1_time_remaining'] == 0: #chip
            if obs['oven_1_recipe'] == 2:
                action = 16
            elif obs['oven_2_recipe'] == 2:
                action = 17
            elif obs['oven_3_recipe'] == 2:
                action = 18
                
        elif obs['baker_3_time_remaining'] == 0: #eclair
            if obs['oven_1_recipe'] == 2:
                action = 19
            elif obs['oven_2_recipe'] == 2:
                action = 20
            elif obs['oven_3_recipe'] == 2:
                action = 21

        elif obs['baker_4_time_remaining'] == 0: #reesee
            if obs['oven_1_recipe'] == 2:
                action = 22
            elif obs['oven_2_recipe'] == 2:
                action = 23
            elif obs['oven_3_recipe'] == 2:
                action = 24
        
        return action
    
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False
    

class MakeCakeController(Controller):
    def __init__(self):
        self.total_time = 0 
        self.obs_history = []
 
    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
    
    def compute_action(self, obs):
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.total_time += 1

        #obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.obs_history.append(obs)
        
        action = 0 

        ## CAKES
        # MIX
        if obs['baker_1_time_remaining'] == 0: #chip
            action = 3
        elif obs['baker_2_time_remaining'] == 0: #coco
            action = 6
        elif obs['baker_3_time_remaining'] == 0: #eclair
            action = 9

        # BAKE
        if obs['baker_1_time_remaining'] == 0: #chip
            if obs['mixer_1_recipe'] == 3:
                action = 10
            elif obs['mixer_2_recipe'] == 3:
                action = 11

        elif obs['baker_2_time_remaining'] == 0: #coco
            if obs['mixer_1_recipe'] == 3:
                action = 12
            elif obs['mixer_2_recipe'] == 3:
                action = 13
                
        elif obs['baker_3_time_remaining'] == 0: #eclair
            if obs['mixer_1_recipe'] == 3:
                action = 14
            elif obs['mixer_2_recipe'] == 3:
                action = 15

        # DECORATE
        if obs['baker_1_time_remaining'] == 0: #chip
            if obs['oven_1_recipe'] == 3:
                action = 16
            elif obs['oven_2_recipe'] == 3:
                action = 17
            elif obs['oven_3_recipe'] == 3:
                action = 18
                
        elif obs['baker_3_time_remaining'] == 0: #eclair
            if obs['oven_1_recipe'] == 3:
                action = 19
            elif obs['oven_2_recipe'] == 3:
                action = 20
            elif obs['oven_3_recipe'] == 3:
                action = 21

        elif obs['baker_4_time_remaining'] == 0: #reesee
            if obs['oven_1_recipe'] == 3:
                action = 22
            elif obs['oven_2_recipe'] == 3:
                action = 23
            elif obs['oven_3_recipe'] == 3:
                action = 24

        
        return action
    
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False
    
class WaitController(Controller):
    def __init__(self):
        self.total_time = 0 
        self.obs_history = []
 
    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]
    
    def compute_action(self, obs):
        sensors_name = [s.name for s in sensors]
        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.total_time += 1

        #obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        self.obs_history.append(obs)
        
        action = 0 
        
        return action
    
    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False