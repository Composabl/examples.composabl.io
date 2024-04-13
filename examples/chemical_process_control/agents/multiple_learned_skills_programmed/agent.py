from asyncore import loop
import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from config import config
from teacher import SS1Teacher, SS2Teacher, TransitionTeacher
from composabl import SkillController

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

class ProgrammedSelector(SkillController):
    def __init__(self):
        self.counter = 0

    async def compute_action(self, obs):
        if self.counter >= 0 and self.counter <= 22:
            action = [0]
        elif self.counter >= 76 :
            action = [2]
        else:
            action = [1]

        return action

    async def transform_obs(self, obs):
        return obs

    async def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False



async def run_agent():
    # Cref_signal is a configuration variable for Concentration and Temperature setpoints
    ss1_scenarios = [
        {
            "Cref_signal": "ss1"
        }
    ]

    ss2_scenarios = [
        {
            "Cref_signal": "ss2"
        }
    ]

    transition_scenarios = [
        {
            "Cref_signal": "transition"
        }
    ]

    selector_scenarios = [
        {
            "Cref_signal": "complete"
        }
    ]

    ss1_skill = Skill("ss1", SS1Teacher)
    for scenario_dict in ss1_scenarios:
        ss1_skill.add_scenario(Scenario(scenario_dict))

    ss2_skill = Skill("ss2", SS2Teacher)
    for scenario_dict in ss2_scenarios:
        ss2_skill.add_scenario(Scenario(scenario_dict))

    transition_skill = Skill("transition", TransitionTeacher)
    for scenario_dict in transition_scenarios:
        transition_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", ProgrammedSelector)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss2_skill, transition_skill, ss1_skill], fixed_order=False, fixed_order_repeat=False)

    # Load a pre-trained agent
    #cleanup_folder(PATH_CHECKPOINTS, ".DS_Store")
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_iters=200)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_agent())
