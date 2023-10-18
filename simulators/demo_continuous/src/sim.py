import gymnasium as gym
import numpy as np
from composabl_core.agent.scenario import Scenario


class SimEnv(gym.Env):
    def __init__(self):
        # Define the initial values
        self.time_ticks = 0
        self.value = 0
        self.is_done = False

        # Define the observation and action spaces
        self.observation_space = self._get_space({
            "state1": {"low": -1e12, "high": 1e12},
            "time_counter": {"low": 0, "high": 1e12},
        })

        self.action_space = self._get_space({
            "action1": {"low": -1e3, "high": 1e3},
        })

        # Define the scenario
        self.scenario: Scenario = None

    @staticmethod
    def _get_space(constraints):
        low_list = [x["low"] for x in constraints.values()]
        high_list = [x["high"] for x in constraints.values()]
        return gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

    def _get_observation(self):
        obs = {"state1": self.value, "time_counter": self.time_ticks}
        return np.array(list(obs.values()))

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
        self.value += action[0]

        #  Update obs with new state values (dummy function)
        obs = self._get_observation()
        reward = 0
        info = {}

        return obs, reward, self.is_done, False, info

    def render_frame(self, mode="auto"):
        pass
