import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from sensors import sensors
from composabl import Teacher
from composabl_core.agent.skill.goals import CoordinatedGoal, MaintainGoal, ApproachGoal,  GoalCoordinationStrategy, MinimizeGoal
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"


class BalanceTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.rms_history = []
        self.last_reward = 0
        self.count = 0

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)


        reward = float(transformed_obs['balance'])
        self.reward_history.append(reward)

        self.count += 1
        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        success = False
        return success

    async def compute_termination(self, transformed_obs, action):
        return False


class GoalTeacher(CoordinatedGoal):
    def __init__(self, *args, **kwargs):
        #navigationx_goal = MaintainGoal("x", "Drive x coordinate to center", target=0, stop_distance=5)
        #navigationy_goal = ApproachGoal("y", " ", target=0, stop_distance=0.1)
        minimize_goal = MinimizeGoal("Conc_Error", " ")
        #y_speed_goal = MaintainGoal("y_speed", " ", target=2, stop_distance=2)

        #super().__init__([navigationx_goal, angle_goal, y_speed_goal, navigationy_goal], GoalCoordinationStrategy.AND)
        super().__init__([minimize_goal])

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref','Conc_Error', 'Eps_Yield', 'Cb_Prod']

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False
