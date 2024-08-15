import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Skill, Trainer
from config import config
from sensors import sensors
from teacher import BaseTeacher

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

def run_agent():
    """Starting the agent."""

    reaction_skill = Skill("reaction", BaseTeacher)
    #for scenario_dict in reaction_scenarios:
    #    reaction_skill.add_scenario(Scenario(scenario_dict))

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    # Load a pre-trained agent
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
