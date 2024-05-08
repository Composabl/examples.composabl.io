import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
#Add the 2 additional teachers below once you have created them in the teacher.py file in the previous step
from teacher import StartReactionTeacher, CSTRTeacher
#Add the 2 additional scenarios below once you have created them in the scenarios.py file in the previous step
from scenarios import start_reaction_scenarios, selector_scenarios
from config import config

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

def run_agent():
    """Starting the agent."""

    #copy this 2 times and past below. Update each skill with the right name, add the relevant Teacher and then the scenarios to complete.
    start_reaction_skill = Skill("start_reaction", StartReactionTeacher)
    for scenario_dict in start_reaction_scenarios:
        start_reaction_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", CSTRTeacher)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)
    #Copy this skill (start_reaction_skill) 2 times and paste below. Update to reflect the names of the skills created above.
    agent.add_skill(start_reaction_skill)


    #Update the selector skill below to include the 2 new skills defined above.
    agent.add_selector_skill(selector_skill, [start_reaction_skill], fixed_order=False, fixed_order_repeat=False)

    # Load a pre-trained agent
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_cycles=2)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()

