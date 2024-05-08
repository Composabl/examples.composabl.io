import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import datetime

from composabl import Agent, Scenario, Skill, Trainer
from config import config
from perceptors import perceptors
from scenarios import bake_scenarios
from sensors import sensors
from teacher import BaseTeacher

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def run_agent():
    start_time = datetime.datetime.now()
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

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)
    agent.add_perceptors(perceptors)

    agent.add_skill(produce_skill)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    if len(files) > 0:
       agent.load(PATH_CHECKPOINTS)


    trainer.train(agent, train_cycles=10)

    agent.export(PATH_CHECKPOINTS)
    end_time = datetime.datetime.now()
    print('Training time: ', end_time - start_time)


if __name__ == "__main__":
    run_agent()

