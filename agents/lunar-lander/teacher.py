import math

from composabl_core.agent import Teacher


class StabilizeTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01
        self.last_reward = 0

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        self.obs_history.append(transformed_obs)
        return 1
        reward = 0
        # has the angle remained stable?
        if abs(self.obs_history[-1][4]) >= abs(transformed_obs[4]) + self.error_tolerance * 180 / math.pi:
            reward += 1
        # has the x position remained stable?
        if abs(self.obs_history[-1][0] - transformed_obs[0]) <= self.error_tolerance * (self.width / self.scale / 2):
            reward += 1
        else:
            reward -= 1
        # has the y position remained stable?
        if abs(self.obs_history[-1][1] - transformed_obs[1]) <= self.error_tolerance * (self.width / self.scale / 2):
            reward += 1
        else:
            reward -= 1
        self.obs_history.append(transformed_obs)
        self.last_reward = reward
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 250

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["position_x", "position_y", "velocity_x", "velocity_y", "theta", "alpha"]


class MoveToCenterTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        VIEWPORT_W = 600
        SCALE = 30.0

        reward = 0
        # if in the center, give a reward
        if abs(transformed_obs[0]) < 0.1:
            reward += 0.5
        else:
            # has the x position moved closer to the center (0)?
            if abs(self.obs_history[-1][0]) - abs(transformed_obs[0]) > 0:
                reward += 1
            else:
                reward -= 1
        # has the y position remained stable?
        if (self.obs_history[-1][1] - transformed_obs[1]) * (VIEWPORT_W / SCALE / 2) < 0.1:
            reward += 1
        else:
            reward -= 1

        # are we level?
        if abs(transformed_obs[4]) * 180 / math.pi < 5:
            reward += 1
        else:
            reward -= 1
        self.obs_history.append(transformed_obs)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 250

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["position_x", "position_y", "velocity_x", "velocity_y", "theta", "alpha"]


class LandTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        VIEWPORT_W = 600
        SCALE = 30.0

        reward = 0
        # has the y position moved closer to the center (0)?
        if abs(self.obs_history[-1][1]) >= abs(transformed_obs[0]) + 0.1 * 180 / math.pi:
            reward += 1
        else:
            reward -= 1
        # has the angle remained stable?
        if abs(self.obs_history[-1][4] - transformed_obs[4]) <= 0.01 * (VIEWPORT_W / SCALE / 2):
            reward += 1
        # has the x position remained stable?
        if abs(self.obs_history[-1][0] - transformed_obs[0]) <= 0.01 * (VIEWPORT_W / SCALE / 2):
            reward += 1
        else:
            reward -= 1
        if abs(self.obs_history[-1][1]) - abs(transformed_obs[1]) >= 0.1 * 180 / math.pi:
            reward -= 2

        # have we landed?
        if transformed_obs[-1] and transformed_obs[-2]:
            reward += 1000
        self.obs_history.append(transformed_obs)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 250

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["position_x", "position_y", "velocity_x", "velocity_y", "theta", "alpha"]


# sparse reward structure
class SelectorTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        reward = 0
        # landed
        if transformed_obs[-1] and transformed_obs[-2]:
            # in the goal!
            if abs(transformed_obs[0]) < 0.15:
                reward += 100
        elif abs(transformed_obs[0]) < 0.15:
            reward += 1
        # has the y position moved closer to the center (0)?
        if abs(self.obs_history[-1][1]) >= abs(transformed_obs[0]) + 0.1 * 180 / math.pi:
            reward += 1
        else:
            reward -= 1
        self.obs_history.append(transformed_obs)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 250

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["position_x", "position_y", "velocity_x", "velocity_y", "theta", "alpha"]
