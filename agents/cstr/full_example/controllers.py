from composabl import Controller


class ControllerSelectControlStrategy(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if self.counter < 22:
            action = [0]
        elif self.counter < 74:  # transition
            action = [1]
        else:
            action = [2]

        self.counter += 1

        return action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ["T", "Tc", "Ca", "Cref", "Tref"]

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False


class ControllerControlReactor(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        self.counter += 1
        return obs["state1"] - 1

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ["state1"]

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False


class ControllerControlToSetPoint(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        self.counter += 1
        return obs["state1"] - 1

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ["state1"]

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False


class RockwellControlToSetPoint(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        self.counter += 1
        return obs["state1"] - 1

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ["state1"]

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False
