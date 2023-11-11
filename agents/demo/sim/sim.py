import gymnasium as gym
import numpy as np
import signal
import sys
from composabl_core.agent.scenario import Scenario


class SimEnv(gym.Env):
    def __init__(self):
        # Define the initial values
        self.time_ticks = 0
        self.value = 0
        self.is_done = False

        # Define the observation and action spaces
        self.observation_space = self._get_space_dict({
            "state1": {"low": -1e12, "high": 1e12},
            "time_counter": {"low": 0, "high": 1e12},
        })

        self.action_space = gym.spaces.Dict({
            "action1": gym.spaces.Discrete(3),
        })

        # Define the scenario
        self.scenario: Scenario = None

    @staticmethod
    def _get_space_dict(constraints):
        space_dictionary = {}
        for name, ranges in constraints.items():
            low = ranges["low"]
            high = ranges["high"]
            space_dictionary[name] = gym.spaces.Box(low=low, high=high, shape=(1,))
        return gym.spaces.Dict(space_dictionary)
    
    @staticmethod
    def _get_space_box(constraints):
        low_list = [x["low"] for x in constraints.values()]
        high_list = [x["high"] for x in constraints.values()]
        return gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))
    
    def _get_observation(self):
        obs = {"state1": self.value, "time_counter": self.time_ticks}
        return obs

    def reset(self):
        self.time_ticks = 0
        self.value = 0

        if isinstance(self.scenario, Scenario):
            self.value = self.scenario.sample()["state1"]

        obs = self._get_observation()
        info = {}

        return obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        # Increase time counting
        self.time_ticks += 1

        # Run Simulation
        print("action", action)
        if action["action1"] == 0:
            self.value -= 1
        elif action["action1"] == 1:
            self.value += 0
        elif action["action1"] == 2:
            self.value += 1

        #  Update obs with new state values (dummy function)
        obs = self._get_observation()
        reward = 0
        info = {}
        return obs, reward, self.is_done, False, info

    def render_frame(self, mode="auto"):
        pass
