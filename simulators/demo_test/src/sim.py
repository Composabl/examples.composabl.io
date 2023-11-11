import gymnasium as gym
import numpy as np
from composabl_core.agent.scenario import Scenario


class SimEnv(gym.Env):
    def __init__(self, space_type="discrete"):
        self.space_type = space_type

        # Define the initial values
        self.time_ticks = 0
        self.value = 0
        self.is_done = False
        self.initial_space = {
            "state1": {"low": -1e12, "high": 1e12},
            "time_counter": {"low": 0, "high": 1e12},
        }

        self.observation_space = self._get_observation_space(self.initial_space)
        self.action_space = self._get_action_space()
        self.action_space = gym.spaces.Discrete(3)

        # Define the scenario
        self.scenario: Scenario = None

    def _get_observation_space(self, constraints):
        if self.space_type == "discrete":
            # for the discrete case, the counting sim doesn't really make sense
            # but since this is just for verifying the SDK supports discrete observations, 
            # the counter sim doesn't have to make sense
            return self._get_space_box(self.initial_space)
        elif self.space_type == "continuous":
            return self._get_space_box(self.initial_space)
        elif self.space_type == "dictionary":
            return self._get_space_dict(self.initial_space)
        elif self.space_type == "tuple":
            return self._get_space_tuple(self.initial_space)
        else:
            raise ValueError(f"Unknown space type {self.space_type}")
    
    def _get_action_space(self):
        if self.space_type == "discrete":
            # for the discrete case, the counting sim doesn't really make sense
            # but since this is just for verifying the SDK supports discrete observations, 
            # the counter sim doesn't have to make sense
            return gym.spaces.Discrete(3)
        elif self.space_type == "continuous":
            return self._get_space_box({
                "action1": {"low": -1e3, "high": 1e3},
            })
        elif self.space_type == "dictionary":
            return gym.spaces.Dict({
                "action1": gym.spaces.Discrete(3),
            })
        elif self.space_type == "tuple":
            return gym.spaces.Tuple([
                gym.spaces.Discrete(3),
            ])
        else:
            raise ValueError(f"Unknown space type {self.space_type}")
    @staticmethod
    def _get_space_discrete(_constraints):
        return gym.spaces.Discrete(3)

    @staticmethod
    def _get_space_box(constraints):
        low_list = [x["low"] for x in constraints.values()]
        high_list = [x["high"] for x in constraints.values()]
        return gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

    @staticmethod
    def _get_space_dict(constraints):
        space_dictionary = {}
        for name, ranges in constraints.items():
            low = ranges["low"]
            high = ranges["high"]
            space_dictionary[name] = gym.spaces.Box(low=low, high=high, shape=(1,))
        return gym.spaces.Dict(space_dictionary)
    
    @staticmethod
    def _get_space_tuple(constraints):
        space_tuple = []
        for name, ranges in constraints.items():
            low = ranges["low"]
            high = ranges["high"]
            space_tuple.append(gym.spaces.Box(low=low, high=high, shape=(1,)))
        return gym.spaces.Tuple(space_tuple)

    def _get_observation_box(self):
        obs = {"state1": self.value, "time_counter": self.time_ticks}
        return np.array(list(obs.values()))

    def _get_observation_dict(self):
        obs = {"state1": self.value, "time_counter": self.time_ticks}
        return obs
    
    def _get_observation_tuple(self):
        obs = (self.value, self.time_ticks)
        return obs
    
    def _get_observation(self):
        if self.space_type == "discrete":
            return self.value
        elif self.space_type == "continuous":
            return self._get_observation_box()
        elif self.space_type == "dictionary":
            return self._get_observation_dict()
        elif self.space_type == "tuple":
            return self._get_observation_tuple()
        else:
            raise ValueError(f"Unknown space type {self.space_type}")

    def _process_action(self, action):
        if self.space_type == "discrete":
            self.value = 1
        elif self.space_type == "continuous":
            self.value +=  action
        elif self.space_type == "dictionary":
            self.value +=  action["action1"]
        elif self.space_type == "tuple":
            self.value =  1
        else:
            raise ValueError(f"Unknown space type {self.space_type}")

    def set_scenario(self, scenario):
        self.scenario = scenario

    def reset(self):
        self.time_ticks = 0
        self.value = 0

        if isinstance(self.scenario, Scenario):
            self.value = self.scenario.sample()["state1"]

        obs = self._get_observation()
        info = {}

        return obs, info


    def step(self, action):
        # Increase time counting
        self.time_ticks += 1

        self._process_action(action)

        #  Update obs with new state values (dummy function)
        obs = self._get_observation()

        # Since this is for testing observation and action space types for the SDK,
        # we don't need to worry about training a logical agent
        # so we can just return a reward of 0
        reward = 0
        info = {}

        return obs, reward, self.is_done, False, info

    def render_frame(self, mode="auto"):
        pass
