import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from composabl import Teacher


class DRLTeacher(Teacher):
    def __init__(self): #(self, *args, **kwargs)
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.count = 0

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return ["y1", "y1ref", "u1", "rms"]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0.0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        temperature = np.mean(np.array(self.obs_history)[:, 0])
        temperature_setpoint = np.mean(np.array(self.obs_history)[:, 1])

        error = abs(temperature - temperature_setpoint)
        reward = 1 / (error)
        self.count += 1
        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        if self.count >= 31:
            return True
        else:
            return False
