from composabl import Teacher


class IncrementTeacher(Teacher):
    def __init__(self):
        self.past_obs = None
        self.counter = 0

    def compute_reward(self, transformed_obs, action, sim_reward):
        self.counter += 1
        if self.past_obs is None:
            self.past_obs = transformed_obs
            return 0
        else:
            if self.past_obs["state1"] < transformed_obs["state1"]:
                return 1
            else:
                return -1

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return self.counter > 100

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["state1", "delta_counter"]


class DecrementTeacher(Teacher):
    def __init__(self):
        self.past_obs = None
        self.counter = 0
        pass

    def compute_reward(self, transformed_obs, action, sim_reward):
        self.counter += 1
        if self.past_obs is None:
            self.past_obs = transformed_obs
            return 0
        else:
            if self.past_obs["state1"] < transformed_obs["state1"]:
                return 1
            else:
                return -1

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return self.counter > 100

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["state1"]


class SelectorTeacher(Teacher):
    def __init__(self):
        self.past_obs = None
        self.counter = 0
        self.target = 15
        pass

    def compute_reward(self, transformed_obs, action, sim_reward):
        self.counter += 1
        if self.past_obs is None:
            self.past_obs = transformed_obs
            return 0
        else:
            if abs(self.target - transformed_obs["state1"]) < abs(self.target - self.past_obs["state1"]):
                return 1
            else:
                return -1

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return self.counter > 100

    def compute_termination(self, transformed_obs, action):
        return False

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        print("transform_action ======", transformed_obs)
        return action

    def filtered_observation_space(self):
        return ["state1"]
