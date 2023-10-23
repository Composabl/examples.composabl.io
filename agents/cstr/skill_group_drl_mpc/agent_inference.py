from composabl.core import Agent, Skill, Sensor, Scenario
from composabl.ray import Runtime
from teacher import CSTRTeacher

from composabl import Controller

import os
import numpy as np

from cstr.external_sim.sim import CSTREnv
import pandas as pd

os.environ["COMPOSABL_EULA_AGREED"] = "1"
license_key = os.environ["COMPOSABL_KEY"]
    
    
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

    control_skill = Skill("control", CSTRTeacher, trainable=True)
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
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(control_skill)

    checkpoint_path = './cstr/skill_group_drl_mpc/saved_agents/'

    #load agent
    agent.load(checkpoint_path)
    agent.train(1)

    #save agent
    trained_agent = agent.prepare()

    # Inference
    sim = CSTREnv()
    sim.scenario = Scenario({
            "Cref_signal": "complete"
        })
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(90):
        action = trained_agent.execute(obs)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break
    
    # save history data
    df.to_pickle("./cstr/skill_group_drl_mpc/inference_data.pkl")  

if __name__ == "__main__":
    start()