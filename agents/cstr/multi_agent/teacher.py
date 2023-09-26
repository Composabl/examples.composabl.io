from composabl import Teacher
import numpy as np
import math

class CSTRTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        error = (transformed_obs['Cref'] - transformed_obs['Ca'])**2
        self.error_history.append(error)
        rms = math.sqrt(np.mean(self.error_history))
        # minimize rms error
        reward = 1 / rms
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history is None:
            return False
        
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False
