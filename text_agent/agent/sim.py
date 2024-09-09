# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import random
import time
from typing import Any, Dict, SupportsFloat, Tuple

import gymnasium as gym
import numpy as np

import composabl_core.utils.logger as logger_util

logger = logger_util.get_logger(__name__)

MAX_COUNTER = 10  # max 8 bit value due to MultiBinary space


class Sim(gym.Env):
    """
    The simulation environment is designed to test and demonstrate how different sensor and
    action space configurations can be implemented and interacted with in RL.

    The goal of the simulation environment is to count to MAX_COUNTER as quickly as possible
    """
    def __init__(self, env_init: dict = {}):
        self.counter = 0  # Initialize counter
        self.steps = 0 # keeps track of epsiode length
        self.sensor_space = gym.spaces.Dict({
            "text": gym.spaces.Text(max_length=16),
            "counter": gym.spaces.Box(low=np.array([0]), high=np.array([MAX_COUNTER]), dtype=np.float32)
        })
        self.action_space = gym.spaces.Discrete(2)  # Increment by 1, or reset to 0

        # Print Debug
        logger.info(f"Initialized Sim (action space: {self.action_space}, obs space: {self.sensor_space})")

    def step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        # Process action
        self.steps += 1
        self._process_action(action)

        # Generate sensor based on space type
        sensors = self._get_sensor()

        # Check if goal is reached
        done = self.steps == MAX_COUNTER
        reward = 1 if done else 0  # Reward when goal is reached

        return sensors, reward, done, False, {}

    def reset(self):
        self.counter = 0
        self.steps = 0

        return self._get_sensor(), {}

    def _process_action(self, action):
        assert self.action_space.contains(action), f"Invalid action {action} not in {self.action_space}. Example: {self.action_space.sample()}"

        # 0 = increment, 1 = decrement
        value_to_add = (1 if action == 0 else -1)

        # Update the counter but ensure it stays within the bounds
        self.counter = max(0, min(MAX_COUNTER, self.counter + value_to_add))

    def _get_sensor(self):
        return self.sensor_space.sample()

    def render_frame(self, mode="human"):
        return f"Counter: {self.counter} \n Text: {self.sensor_space['text'].sample()}"
