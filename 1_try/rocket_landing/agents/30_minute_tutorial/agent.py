import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from config import config
from sensors import sensors
from scenarios import Navigation_scenarios
from teacher import (NavigationTeacher, SpeedControlTeacher,
                     StabilizationTeacher)

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

# Change here to define how the agent will orchestrate each skill
# Define the Programmed Selector and how it selects the each skill
class ProgrammedSelector(Controller):
    def __init__(self, *args, **kwargs):
        self.counter = 0

    def compute_action(self, obs):
        if abs(float(obs['angle'])) > 0.5:
            return [1] #"Stabilization_skill"

        elif abs(float(obs['x'])) > 10:
            return [0] #"Navigation_skill"

        else:
            return [2] #"SpeedControl_skill"

    def transform_sensors(self, obs):
        return obs

    def filtered_observation_space(self):
        return [s.name for s in sensors]

    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False


def run_agent():
    # Define Skills
    Navigation_skill = Skill("Navigation", NavigationTeacher)
    SpeedControl_skill = Skill("SpeedControl", SpeedControlTeacher)
    Stabilization_skill = Skill("Stabilization", StabilizationTeacher)
    selector_skill = Skill("selector", ProgrammedSelector)

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)
        SpeedControl_skill.add_scenario(scenario)
        Stabilization_skill.add_scenario(scenario)
        selector_skill.add_scenario(scenario)

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    # Add individual skills to the agent
    agent.add_skill(Navigation_skill)
    agent.add_skill(SpeedControl_skill)
    agent.add_skill(Stabilization_skill)

    # Add the selector skill to the agent
    agent.add_selector_skill(selector_skill, [Navigation_skill, Stabilization_skill, SpeedControl_skill], fixed_order=False)

    # Load a pre-trained agent
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_cycles=100)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()
