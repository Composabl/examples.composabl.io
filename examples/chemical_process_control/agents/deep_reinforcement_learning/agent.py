import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from composabl import Agent, Runtime, Scenario, Skill
from sensors import sensors
from teacher import CSTRTeacher

from utils.cleanup import cleanup_folder
from utils.config import generate_config

license_key = os.environ["COMPOSABL_LICENSE"]

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

def start():
    """Starting the agent."""

    if DELETE_OLD_HISTORY_FILES:
        cleanup_folder(PATH_HISTORY)
    else:
        print("|-- Skipping deletion of old history files...")

    # `Cref_signal` is a configuration variable for concentration
    # and temperature set points.
    reaction_scenarios = [{"Cref_signal": "complete"}]

    reaction_skill = Skill("reaction", CSTRTeacher)
    for scenario_dict in reaction_scenarios:
        reaction_skill.add_scenario(Scenario(scenario_dict))

    DOCKER_IMAGE: str = "composabl/sim-cstr:latest"

    config = generate_config(
        license_key=license_key,
        target="docker",
        image=DOCKER_IMAGE,
        env_name="sim-cstr",
        workers=1,
        num_gpus=0,
    )

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    # Load a pre-trained agent
    cleanup_folder(PATH_CHECKPOINTS, ".DS_Store")
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_iters=5)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
