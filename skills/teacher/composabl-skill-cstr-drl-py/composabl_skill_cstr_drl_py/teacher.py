# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import math
from typing import List
from composabl_core import SkillTeacher


class Teacher(SkillTeacher):
    """
    We start at 10 reward and count down to 0 the goal is that the agent stays
    above or equal to 0 this means it learned to cound +1 each time
    """

    def __init__(self):
        self.past_obs = None
        self.counter = 10
        self.sensor_name = "counter"

    async def compute_reward(self, transformed_obs, action, sim_reward):
        """
        The reward increases the closer it gets to 10, but decreases the
        further it gets from 10 it decreases faster the further it gets

        note: we do this through a piecewise function, where the reward is
        100 if the counter is 10 and 0 if the counter is 0 everything above
        10 gets a steep decrease and everything below 10 gets a small increase

        ASCII of the Piecewise Graph

                      ***********
                 *****           ***
              ***                   **
            **                        **
         ***                            **
        *                                 *
                                           **
                                             *
                                              *
                                               *
        """
        counter = transformed_obs[self.sensor_name]

        # Small build up if < 10
        # given by e^(counter - 10) + 100
        if counter < 10:
            return math.exp(counter - 10) + 100
        # else steep decent after max reward
        # given by -2 * e^(-|counter - 10|) + 100
        else:
            return -2 * math.exp(-abs(counter - 10)) + 100

    async def compute_action_mask(self, transformed_obs, action) -> List[bool]:
        return None

    async def compute_success_criteria(self, transformed_obs, action) -> bool:
        return bool(transformed_obs[self.sensor_name] >= 10)

    async def compute_termination(self, transformed_obs, action) -> bool:
        return bool(transformed_obs[self.sensor_name] <= -10)

    async def transform_obs(self, obs, action) -> str:
        return obs

    async def transform_action(self, transformed_obs, action) -> float:
        return action

    async def filtered_observation_space(self) -> List[str]:
        return [self.sensor_name]
