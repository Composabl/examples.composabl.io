import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sensors import sensors
from composabl import SkillController

class ProgrammedSelector(SkillController):
    def __init__(self):
        self.counter = 0

    async def compute_action(self, obs):
        if abs(float(obs['angle'])) > 0.5:
            return [1] #"Stabilization_skill"

        elif abs(float(obs['x'])) > 10:
            return [0] #"Navigation_skill"

        else:
            return [2] #"SpeedControl_skill"

    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False
