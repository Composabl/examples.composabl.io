from composabl.core import Agent, Skill, Sensor, Scenario
from composabl.ray import Runtime
#from .reward import stabilize_reward, move_to_center_reward, land_reward, base_reward

from composabl_core.agent import Teacher

import numpy as np

import os

license_key = os.environ["COMPOSABL_KEY"]
    
class TemperatureControlTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["y1", "y1ref", "u1", "rms"]

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        temperature = np.mean(np.array(self.obs_history)[:,0])
        temperature_setpoint = np.mean(np.array(self.obs_history)[:,1])

        error = abs(temperature - temperature_setpoint)
        reward = 1 / (error)
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False

def start():
    y1 = Sensor("y1", "Temperature")
    y1ref = Sensor("y1ref", "")
    u1 = Sensor("u1", "")
    rms = Sensor("rms", "")

    sensors = [y1, y1ref, u1, rms]

    TemperatureControl_scenarios = [
        {
            "y1_SP": 170,
            "time_delay": 0.028
        }
    ]

    TemperatureControl_skill = Skill("TemperatureControl", TemperatureControlTeacher, trainable=True)

    for scenario_dict in TemperatureControl_scenarios:
        scenario = Scenario(scenario_dict)
        TemperatureControl_skill.add_scenario(scenario)

    config = {
        "env": {
            "name": "filament_extruder",
            "compute": "local",  # "docker", "kubernetes", "local"
            "strategy": "local",  # "docker", "kubernetes", "local"
            "config": {
                "address": "localhost:1337",
                # "image": "composabl.ai/sim-gymnasium:latest"
            }
        },
        "license": license_key,
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(TemperatureControl_skill)

    agent.train(train_iters=3)
