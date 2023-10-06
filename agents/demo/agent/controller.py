from composabl import Controller


class DecrementController(Controller):
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


class IncrementController(Controller):
    def __init__(self):
        self.counter = 0
        
    def compute_action(self, obs):
        self.counter += 1
        return obs["state1"] + 1

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ["state1"]

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False
    
class SelectorController(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        self.counter += 1
        return 0  # always choose the first child to do an action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ["state1"]
    
    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False