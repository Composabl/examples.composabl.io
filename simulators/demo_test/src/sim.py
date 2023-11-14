from venv import logger
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

        if self.space_type == "discrete":
            self.observation_space = gym.spaces.Discrete(2)
            self.action_space = gym.spaces.Discrete(3)
        elif self.space_type == "multi_discrete":
            self.observation_space = gym.spaces.MultiDiscrete([2, 3])
            self.action_space = gym.spaces.MultiDiscrete([3, 2])
        elif self.space_type == "multibinary":
            self.observation_space = gym.spaces.MultiBinary(2)
            self.action_space = gym.spaces.MultiBinary(3)
        elif self.space_type == "box":
            self.observation_space = gym.spaces.Box(
                low=np.array([-1e12, -1e12]), high=np.array([1e12, 1e12]),
                dtype=np.uint8)
            self.action_space = gym.spaces.Box(
                low=np.array([-1e12]), high=np.array([1e12])
            )
        elif self.space_type == "dictionary":
            self.observation_space = gym.spaces.Dict({
                "state1": gym.spaces.Box(
                    low=np.array([-1e12]), high=np.array([1e12]),),
                "time_counter": gym.spaces.Discrete(5),
            })
            self.action_space = gym.spaces.Dict({
                "action1": gym.spaces.Discrete(3),
                "action2": gym.spaces.Box(low=np.array([-1e12]), high=np.array([1e12]))
            })

        elif self.space_type == "tuple":
            self.observation_space = gym.spaces.Tuple([
                gym.spaces.Box(low=np.array([-1e12]), high=np.array([1e12]),),
                gym.spaces.Discrete(5),
            ])
            self.action_space = gym.spaces.Tuple([
                gym.spaces.Discrete(3),
                gym.spaces.Box(low=np.array([-1e12]), high=np.array([1e12])),
            ])

        # Define the scenario
        self.scenario: Scenario = None

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
        elif self.space_type == "multi_discrete":
            return [2, 1]
        elif self.space_type == "multibinary":
            return [0, 1]
        elif self.space_type == "box":
            return self._get_observation_box()
        elif self.space_type == "dictionary":
            return self._get_observation_dict()
        elif self.space_type == "tuple":
            return self._get_observation_tuple()
        else:
            raise ValueError(f"Unknown space type {self.space_type}")

    def _process_action(self, action):
        if self.space_type in ["discrete", "multi_discrete", "multibinary"]:
            self.value = 1
        elif self.space_type == "box":
            self.value = action[0]
        elif self.space_type == "dictionary":
            self.value = action["action1"]
        elif self.space_type == "tuple":
            self.value = action[1]
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
