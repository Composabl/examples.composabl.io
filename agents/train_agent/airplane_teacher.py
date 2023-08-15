import math

from composabl_core.agent import Teacher

class NavigationTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["y1", "y2", "u1", "u2", "u3", "u4"]

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        e1 = 0.001 if (-9.5 < transformed_obs["y1"] < -8.5) else abs(transformed_obs["y1"] - ((-9.5 + -8.5) / 2))  # (-9.5,-8.5)
        e2 = 0.001 if (4.6 < transformed_obs["y2"] < 5.4) else abs(transformed_obs["y2"] - ((4.6 + 5.4) / 2))  # (4.6,5.4)

        reward = float(1 / (e1 + e2))

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False