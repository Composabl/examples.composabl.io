import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Skill
from sensors import sensors
from config import config
from scenarios import bake_scenarios
from teacher import BaseTeacher

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def run_agent():
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]

        for file in pkl_files:
            file_path = PATH_HISTORY + '/' + file
            os.remove(file_path)
    except:
        pass

    produce_skill = Skill("produce", BaseTeacher)
    for scenario_dict in bake_scenarios:
        produce_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(produce_skill)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')


    if len(files) > 0:
        agent.load(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=2)

    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()

