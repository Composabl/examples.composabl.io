import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import StartReactionTeacher, CSTRTeacher
from scenarios import start_reaction_scenarios, selector_scenarios
from config import config

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

def run_agent():
    """Starting the agent."""

    start_reaction_skill = Skill("start_reaction", StartReactionTeacher)
    for scenario_dict in start_reaction_scenarios:
        start_reaction_skill.add_scenario(Scenario(scenario_dict))
    
    selector_skill = Skill("selector", CSTRTeacher)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(start_reaction_skill)
    agent.add_selector_skill(selector_skill, [start_reaction_skill], fixed_order=False, fixed_order_repeat=False)
   
    # Load a pre-trained agent
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_iters=2)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()

