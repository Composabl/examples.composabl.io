import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Trainer, Scenario, Skill
from teacher import TemperatureControlTeacher
from sensors import sensors
from config import config
from scenarios import TemperatureControl_scenarios

from teacher import TemperatureControlTeacher

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

def run_agent():
    TemperatureControl_skill = Skill("TemperatureControl", TemperatureControlTeacher)

    for scenario_dict in TemperatureControl_scenarios:
        scenario = Scenario(scenario_dict)
        TemperatureControl_skill.add_scenario(scenario)

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(TemperatureControl_skill)

    trainer.train(agent, train_cycles=3)


if __name__ == "__main__":
    run_agent()
