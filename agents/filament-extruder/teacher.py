import numpy as np
from composabl import Teacher


class TemperatureControlTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["y1", "y1ref", "u1", "rms"]

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        temperature = np.mean(np.array(self.obs_history)[:, 0])
        temperature_setpoint = np.mean(np.array(self.obs_history)[:, 1])

        error = abs(temperature - temperature_setpoint)
        reward = 1 / (error)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False
