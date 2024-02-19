import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from composabl import Agent, Runtime, Scenario, Skill
from teacher import LevelTeacher, PressureTeacher, TemperatureTeacher
from sensors import sensors

from utils.config import generate_config
from utils.cleanup import cleanup_folder

# Constants for setting up execution environment
LICENSE_KEY = os.environ["COMPOSABL_LICENSE"]
PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"
DELETE_OLD_HISTORY_FILES: bool = True


def start():
    """Starting the agent."""

    if DELETE_OLD_HISTORY_FILES:
        print("|-- Deleting old history files...")
        cleanup_folder(PATH_HISTORY)
    else:
        print("|-- Skipping deletion of old history files...")

    # Setting up scenarios for each skill
    y1_scenarios = [{"signal": "y1", "eff_nox_red": 0.7}]
    level_skill = Skill("Level", LevelTeacher)
    for scenario_dict in y1_scenarios:
        scenario = Scenario(scenario_dict)
        level_skill.add_scenario(scenario)

    y2_scenarios = [{"signal": "y2", "eff_nox_red": 0.7}]
    pressure_skill = Skill("Pressure", PressureTeacher)
    for scenario_dict in y2_scenarios:
        scenario = Scenario(scenario_dict)
        pressure_skill.add_scenario(scenario)

    y3_scenarios = [{"signal": "y3", "eff_nox_red": 0.7}]
    temperature_skill = Skill("Temperature", TemperatureTeacher)
    for scenario_dict in y3_scenarios:
        scenario = Scenario(scenario_dict)
        temperature_skill.add_scenario(scenario)

    # Setting up the runtime and agent configuration
    config = generate_config(
        license_key=LICENSE_KEY,
        target="local",
        image="composabl/sim-boiler-local",
        env_name="industrial-boiler",
        workers=4,
        num_gpus=0,
        training={},
    )

    runtime = Runtime(config)

    agent = Agent()
    agent.add_sensors(sensors)
    agent.add_skill(level_skill)
    #agent.add_skill(pressure_skill)
    #agent.add_skill(temperature_skill)


    cleanup_folder(PATH_CHECKPOINTS, ".DS_Store")

    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    runtime.train(agent, train_iters=5)

    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
