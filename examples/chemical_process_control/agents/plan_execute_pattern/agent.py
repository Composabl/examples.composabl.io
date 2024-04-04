import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Skill, Sensor, Scenario, Controller, Runtime
from teacher import CSTRTeacher
from sensors import sensors
from config import config
from scenarios import reaction_scenarios

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

def run_agent():
    control_skill = Skill("control", CSTRTeacher)
    for scenario_dict in reaction_scenarios:
        control_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(control_skill)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    if len(files) > 0:
        agent.load(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=1)

    #save agent
    agent.export(PATH_CHECKPOINTS)

if __name__ == "__main__":
    run_agent()
