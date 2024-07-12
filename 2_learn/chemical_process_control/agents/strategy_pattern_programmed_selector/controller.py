from composabl import SkillController

class ProgrammedSelector(SkillController):
    def __init__(self, *args, **kwargs):
        self.counter = 0

    async def compute_action(self, obs, action):
        self.counter += 1
        if self.counter >= 0 and self.counter <= 22:
            action = 0
        elif self.counter >= 76 :
            action = 2
        else:
            action = 1

        return action

    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False

