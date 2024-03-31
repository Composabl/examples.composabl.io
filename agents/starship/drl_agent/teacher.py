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
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        error_1 = abs((0 - float(transformed_obs["x"]) )/400)
        error_2 = abs((0 - float(transformed_obs["x_speed"]))/100)
        error_3 = abs((0 - float(transformed_obs["y"]) )/1000)
        error_4 = abs((5 - float(transformed_obs["y_speed"]))/1000)
        error_5 = abs((0 - float(transformed_obs["angle"]))/3.15)
        error_6 = abs((0 - float(transformed_obs["ang_speed"]))/1)

        reward = 0.3 * error_1 + 0.1 * error_2 + 0.3 * error_3 + 0.1 * error_4 + 0.1 * error_5 + 0.1 * error_6

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False
