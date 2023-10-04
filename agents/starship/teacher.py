from composabl import Teacher


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
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        normalized_x = abs(transformed_obs["x"] / 400)
        normalized_x_speed = abs(transformed_obs["x_speed"] / 100)
        normalized_y = transformed_obs["y"] / 1000
        normalized_y_speed = abs(transformed_obs["y_speed"] / 1000)
        normalized_angle = abs(transformed_obs["angle"] / 3.15)
        normalized_angle_speed = abs(transformed_obs["ang_speed"] / 1)

        reward = 0.3 * (1 - normalized_x) + 0.1 * (1 - normalized_x_speed) + 0.3 * (1 - normalized_y) + 0.1 * (1 - normalized_y_speed) + 0.1 * (1 - normalized_angle) + 0.1 * (1 - normalized_angle_speed)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class AlignmentTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        normalized_x = abs(transformed_obs["x"] / 400)
        normalized_x_speed = abs(transformed_obs["x_speed"] / 100)
        normalized_y = transformed_obs["y"] / 1000
        normalized_y_speed = abs(transformed_obs["y_speed"] / 1000)
        normalized_angle = abs(transformed_obs["angle"] / 3.15)
        normalized_angle_speed = abs(transformed_obs["ang_speed"] / 1)

        reward = 0.1 * (1 - normalized_x) + 0.1 * (1 - normalized_x_speed)\
            + 0.1 * (1 - normalized_y) + 0.1 * (1 - normalized_y_speed) \
            + 0.3 * (1 - normalized_angle) + 0.3 * (1 - normalized_angle_speed)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class SpeedControlTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        normalized_x = abs(transformed_obs["x"] / 400)
        normalized_x_speed = abs(transformed_obs["x_speed"] / 100)
        normalized_y = transformed_obs["y"] / 1000
        normalized_y_speed = abs(transformed_obs["y_speed"] / 1000)
        normalized_angle = abs(transformed_obs["angle"] / 3.15)
        normalized_angle_speed = abs(transformed_obs["ang_speed"] / 1)

        reward = 0.1 * (1 - normalized_x) + 0.25 * (1 - normalized_x_speed)\
            + 0.1 * (1 - normalized_y) + 0.25 * (1 - normalized_y_speed) \
            + 0.15 * (1 - normalized_angle) + 0.15 * (1 - normalized_angle_speed)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class StabilizationTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        normalized_x = abs(transformed_obs["x"] / 400)
        normalized_x_speed = abs(transformed_obs["x_speed"] / 100)
        normalized_y = transformed_obs["y"] / 1000
        normalized_y_speed = abs(transformed_obs["y_speed"] / 1000)
        normalized_angle = abs(transformed_obs["angle"] / 3.15)
        normalized_angle_speed = abs(transformed_obs["ang_speed"] / 1)

        reward = 0.1 * (1 - normalized_x) + 0.15 * (1 - normalized_x_speed)\
            + 0.1 * (1 - normalized_y) + 0.15 * (1 - normalized_y_speed) \
            + 0.25 * (1 - normalized_angle) + 0.25 * (1 - normalized_angle_speed)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False
