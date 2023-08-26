import numpy as np
from composabl import Teacher


class LevelTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['y1', 'y2', 'y3', 'y1ref', 'y2ref', 'y3ref', 'u1', 'u2', 'u3']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        error = abs(np.mean(np.array(self.obs_history)[:, 0]) - np.mean(np.array(self.obs_history)[:, 3]))

        if error != 0:
            reward = 1 / error
        else:
            reward = 1e12

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class PressureTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['y1', 'y2', 'y3', 'y1ref', 'y2ref', 'y3ref', 'u1', 'u2', 'u3']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        error = abs(np.mean(np.array(self.obs_history)[:, 1]) - np.mean(np.array(self.obs_history)[:, 4]))

        if error != 0:
            reward = 1 / error
        else:
            reward = 1e12

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class TemperatureTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['y1', 'y2', 'y3', 'y1ref', 'y2ref', 'y3ref', 'u1', 'u2', 'u3']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        error = abs(np.mean(np.array(self.obs_history)[:, 2]) - np.mean(np.array(self.obs_history)[:, 5]))

        if error != 0:
            reward = 1 / error
        else:
            reward = 1e12

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False
