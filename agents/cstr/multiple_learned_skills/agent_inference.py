import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher

from cstr.external_sim.sim import CSTREnv
import pandas as pd
import numpy as np

license_key = os.environ["COMPOSABL_KEY"]


def start():
    # delete old history files
    dir = './cstr/multiple_learned_skills'
    files = os.listdir(dir)
    pkl_files = [file for file in files if file.endswith('inference_data.pkl')]
    for file in pkl_files:
        file_path = os.path.join(dir, file)
        os.remove(file_path)

    T = Sensor("T", "")
    Tc = Sensor("Tc", "")
    Ca = Sensor("Ca", "")
    Cref = Sensor("Cref", "")
    Tref = Sensor("Tref", "")

    sensors = [T, Tc, Ca, Cref, Tref]

    # Cref_signal is a configuration variable for Concentration and Temperature setpoints
    ss1_scenarios = [
        {
            "Cref_signal": "ss1"
        }
    ]

    ss2_scenarios = [
        {
            "Cref_signal": "ss2"
        }
    ]

    transition_scenarios = [
        {
            "Cref_signal": "transition"
        }
    ]

    selector_scenarios = [
        {
            "Cref_signal": "complete"
        }
    ]

    ss1_skill = Skill("ss1", SS1Teacher, trainable=True)
    for scenario_dict in ss1_scenarios:
        ss1_skill.add_scenario(Scenario(scenario_dict))

    ss2_skill = Skill("ss2", SS2Teacher, trainable=True)
    for scenario_dict in ss2_scenarios:
        ss2_skill.add_scenario(Scenario(scenario_dict))

    transition_skill = Skill("transition", TransitionTeacher, trainable=True)
    for scenario_dict in transition_scenarios:
        transition_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", CSTRTeacher, trainable=True)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

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

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-cstr:latest"
            }
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "ray": {
                "workers": 1
            }
        }
    }

    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss1_skill, transition_skill, ss2_skill], fixed_order=False, fixed_order_repeat=False)

    checkpoint_path = './cstr/multiple_learned_skills/saved_agents/'

    #load agent
    agent.load(checkpoint_path)
    #agent.train(1)

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
        #action = np.array(action[0]*10)
        action = np.array((action[0]+10)/20)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break
    
    # save history data
    df.to_pickle("./cstr/multiple_learned_skills/inference_data.pkl")  


if __name__ == "__main__":
    start()
