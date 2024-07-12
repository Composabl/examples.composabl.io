import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Scenario, Skill, SkillSelector, Trainer
from config import config
from scenarios import (
    selector_scenarios,
    ss1_scenarios,
    ss2_scenarios,
    transition_scenarios,
)
from sensors import sensors
from teacher import SS1Teacher, SS2Teacher, TransitionTeacher
from controller import ProgrammedSelector

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def run_agent():
    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    with SkillSelector("selector", ProgrammedSelector) as selector_skill:
        for selector_scenario in selector_scenarios:
            selector_skill.add_scenario(Scenario(selector_scenario))

        with Skill("ss2", SS2Teacher) as ss2_skill:
            for scenario_dict in ss2_scenarios:
                ss2_skill.add_scenario(Scenario(scenario_dict))
            selector_skill.add_skill(ss2_skill)

        with Skill("ss1", SS1Teacher) as ss1_skill:
            for scenario_dict in ss1_scenarios:
                ss1_skill.add_scenario(Scenario(scenario_dict))
            selector_skill.add_skill(ss1_skill)

        with Skill("transition", TransitionTeacher) as transition_skill:
            for scenario_dict in transition_scenarios:
                transition_skill.add_scenario(Scenario(scenario_dict))
            selector_skill.add_skill(transition_skill)


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
