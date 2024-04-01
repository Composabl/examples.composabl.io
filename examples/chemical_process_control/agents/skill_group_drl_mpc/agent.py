from composabl.core import Agent, Skill, Sensor, Scenario
from composabl.ray import Runtime
from teacher import CSTRTeacher

from composabl import Controller

import os
import numpy as np

os.environ["COMPOSABL_EULA_AGREED"] = "1"
license_key = os.environ["COMPOSABL_LICENSE"]


def start():
    T = Sensor("T", "")
    Tc = Sensor("Tc", "")
    Ca = Sensor("Ca", "")
    Cref = Sensor("Cref", "")
    Tref = Sensor("Tref", "")

    sensors = [T, Tc, Ca, Cref, Tref]

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
            "local": {
            "address": "localhost:1337"
            }
        },
        "env": {
            "name": "sim-cstr",
        },

        "flags": {
            "print_debug_info": True
        },
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(control_skill)

    checkpoint_path = './cstr/skill_group_drl_mpc/saved_agents/'

    try:
        files = os.listdir(PATH_CHECKPOINTS)

        if '.DS_Store' in files:
            files.remove('.DS_Store')
            os.remove(PATH_CHECKPOINTS + '/.DS_Store')

        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)

    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=1)

    #save agent
    agent.export(checkpoint_path)

if __name__ == "__main__":
    start()
