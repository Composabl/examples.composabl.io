import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher
from scenarios import ss1_scenarios, ss2_scenarios, transition_scenarios, selector_scenarios
from config import config

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

def run_agent():
    """Starting the agent."""

    ss1_skill = Skill("ss1", SS1Teacher)
    for scenario_dict in ss1_scenarios:
        ss1_skill.add_scenario(Scenario(scenario_dict))

    ss2_skill = Skill("ss2", SS2Teacher)
    for scenario_dict in ss2_scenarios:
        ss2_skill.add_scenario(Scenario(scenario_dict))

    transition_skill = Skill("transition", TransitionTeacher)
    for scenario_dict in transition_scenarios:
        transition_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", CSTRTeacher)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss1_skill, transition_skill, ss2_skill], fixed_order=False, fixed_order_repeat=False)

    # Load a pre-trained agent
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_iters=120)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()

