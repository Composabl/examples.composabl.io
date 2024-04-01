from asyncore import loop
import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from composabl import Agent, Runtime, Scenario, Skill
from sensors import sensors
from config import config
from scenarios import reaction_scenarios
from teacher import CSTRTeacher

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

async def start():
    """Starting the agent."""

    reaction_skill = Skill("reaction", CSTRTeacher)
    for scenario_dict in reaction_scenarios:
        reaction_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    # Load a pre-trained agent
    #cleanup_folder(PATH_CHECKPOINTS, ".DS_Store")
    #try:
    #    if len(os.listdir(PATH_CHECKPOINTS)) > 0:
    #        agent.load(PATH_CHECKPOINTS)
    #except Exception:
    #    print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    await runtime.train(agent, train_iters=5)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
