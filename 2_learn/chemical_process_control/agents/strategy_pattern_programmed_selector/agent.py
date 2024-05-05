import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Scenario, Skill, SkillController, Trainer
from config import config
from scenarios import (
    selector_scenarios,
    ss1_scenarios,
    ss2_scenarios,
    transition_scenarios,
)
from sensors import sensors
from teacher import SS1Teacher, SS2Teacher, TransitionTeacher

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

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

    async def filtered_sensor_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False



def run_agent():
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

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss2_skill, transition_skill, ss1_skill], fixed_order=False, fixed_order_repeat=False)

    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    trainer.train(agent, train_cycles=100)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()
