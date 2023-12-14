from composabl.core import Agent, Skill, Sensor, Scenario
from composabl.ray import Runtime
from teacher import CSTRTeacher
from sensors import sensors
from composabl import Controller

import os
import numpy as np

os.environ["COMPOSABL_EULA_AGREED"] = "1"
license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/saved_agents"

def start():
    # delete old history files
    dir = './cstr/skill_group_drl_mpc'
    files = os.listdir(dir)
    pkl_files = [file for file in files if file.endswith('.pkl')]
    for file in pkl_files:
        file_path = os.path.join(dir, file)
        os.remove(file_path)

    # Cref_signal is a configuration variable for Concentration and Temperature setpoints
    control_scenarios = [
        {
            "Cref_signal": "complete",
            "noise_percentage": 0.0
        }
    ]

    control_skill = Skill("control", CSTRTeacher)
    for scenario_dict in control_scenarios:
        control_skill.add_scenario(Scenario(scenario_dict))

    config = {
        "license": license_key,
        "target": {
            #"local": {
            #    "address": "localhost:1337"
            #},
            "docker": {
                "image": "composabl/sim-cstr:latest"
            },
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "ray": {
                "workers": 8
            }
        },
        "flags": {
            "print_debug_info": True
        },
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(control_skill)

    '''try:
        files = os.listdir(PATH_CHECKPOINTS)

        if '.DS_Store' in files:
            files.remove('.DS_Store')

        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)'''

    runtime.train(agent, train_iters=10)

    #save agent
    #agent.export(PATH_CHECKPOINTS)

if __name__ == "__main__":
    start()
