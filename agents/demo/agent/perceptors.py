from composabl import Perceptor


class DeltaCounter():
    def __init__(self):
        self.key = "state1"
        self.previous_value = None

    def compute(self, obs):
        if self.previous_value is None:
            self.previous_value = obs[self.key]
            return {"delta_counter": 0, "state2": 0}
        
        delta = obs["state1"] - self.previous_value
        self.previous_value = obs["state1"]
        return {"delta_counter": delta, "state2": 0}
    
    def filtered_observation_space(self, obs):
        return ["state1"]


delta_counter = Perceptor("perceptor1", DeltaCounter, "the change in the counter from the last two steps")

perceptors = [delta_counter]
