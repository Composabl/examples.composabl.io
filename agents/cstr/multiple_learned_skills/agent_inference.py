import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher
from sensors import sensors
from cstr.external_sim.sim import CSTREnv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

license_key = os.environ["COMPOSABL_LICENSE"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def start():
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

    ss1_skill = Skill("ss1", SS1Teacher)
    for scenario_dict in ss1_scenarios:
        ss1_skill.add_scenario(Scenario(scenario_dict))

    ss2_skill = Skill("ss2", SS2Teacher)
    for scenario_dict in ss2_scenarios:
        ss2_skill.add_scenario(Scenario(scenario_dict))

    transition_skill = Skill("transition", TransitionTeacher)
    for scenario_dict in transition_scenarios:
        transition_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", CSTRTeacher)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-cstr:latest"
            },
            #"local": {
            #    "address": "localhost:1337"
            #}
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
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss1_skill, transition_skill, ss2_skill], fixed_order=False, fixed_order_repeat=False)

    #load agent
    agent.load(PATH_CHECKPOINTS)

    #save agent
    trained_agent = runtime.package(agent)

    # Inference
    noise = 0.05
    sim = CSTREnv()
    sim.scenario = Scenario({
            "Cref_signal": "complete",
            "noise_percentage": noise
        })
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(90):
        action = trained_agent.execute(obs)
        action = np.array((action[0]+10)/20)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break

    # save history data
    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(3,1,1)
    plt.plot(df.reset_index()['time'],df.reset_index()['Tc'])
    plt.ylabel('Tc')
    plt.legend(['reward'],loc='best')
    plt.title('Agent Inference Multiple Learned Skills' + f" - Noise: {noise}")

    plt.subplot(3,1,2)
    #plt.plot(self.rms_history, 'r.-')
    plt.plot(df.reset_index()['time'],df.reset_index()['T'])
    plt.plot(df.reset_index()['time'],df.reset_index()['Tref'],'r--')
    plt.ylabel('Temp')
    plt.legend(['T', 'Tref'],loc='best')

    plt.subplot(3,1,3)
    plt.plot(df.reset_index()['time'],df.reset_index()['Ca'])
    plt.plot(df.reset_index()['time'],df.reset_index()['Cref'],'r--')
    plt.legend(['Ca', 'Cref'],loc='best')
    plt.ylabel('Concentration')
    plt.xlabel('iteration')

    plt.savefig(f"{PATH}/img/inference_figure.png")


if __name__ == "__main__":
    start()
