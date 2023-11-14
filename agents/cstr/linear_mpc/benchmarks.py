import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from controller import MPCController

from cstr.external_sim.sim import CSTREnv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

license_key = os.environ["COMPOSABL_KEY"]


def start():
    T = Sensor("T", "")
    Tc = Sensor("Tc", "")
    Ca = Sensor("Ca", "")
    Cref = Sensor("Cref", "")
    Tref = Sensor("Tref", "")

    sensors = [T, Tc, Ca, Cref, Tref]

    # Cref_signal is a configuration variable for Concentration and Temperature setpoints
    reaction_scenarios = [
        {
            "Cref_signal": "complete",
            "noise_percentage": 0.01
        }
    ]

    reaction_skill = Skill("reaction", MPCController, trainable=False)
    for scenario_dict in reaction_scenarios:
        reaction_skill.add_scenario(Scenario(scenario_dict))

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

    agent.add_skill(reaction_skill)

    # Inference
    noise = 0.05

    df = pd.DataFrame()

    for j in range(3):
        sim = CSTREnv()
        sim.scenario = Scenario({
                "Cref_signal": "complete",
                "noise_percentage": noise
            })
        cont = MPCController()
        obs, info = sim.reset()
        for i in range(90-1):
            action = cont.compute_action(obs)
            obs, reward, done, truncated, info = sim.step(action)
            df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
            df = pd.concat([df, df_temp])

            if done:
                break

    # calculate error
    df['error_temp'] = (df['T'] - df['Tref'])**2
    df['error_conc'] = (df['Ca'] - df['Cref'])**2
    rmsT = round(np.sqrt(np.mean(df['error_temp'])),2)
    rmsCa = round(np.sqrt(np.mean(df['error_conc'])),2)
    print('RMS T: ', rmsT)
    print('RMS Ca: ', rmsCa)

    plt.subplot(2,1,1)
    Tr_list_ = df.set_index('time')['T']
    Tref_list = df.set_index('time')['Tref'][:90]
    min_Tr = [min(np.array(Tr_list_[i])) for i in range(90)]
    max_Tr = [max(np.array(Tr_list_[i])) for i in range(90)]
    mean_Tr = [np.mean(np.array(Tr_list_[i])) for i in range(90)]
    plt.fill_between([i for i in range(90)] , min_Tr , max_Tr, alpha = 0.2)
    plt.plot([i for i in range(90)],Tref_list,'k--',lw=2,label=r'$T_{sp}$')
    plt.plot([i for i in range(90)],mean_Tr,'b.-',lw=1,label=r'$T_{sp}$')
    plt.plot([i for i in range(90)],[400 for x in range(90)],'r--',lw=1)
    plt.ylabel('Temperature')
    plt.title(f'Benchmarks Noise: {noise}' + f" (RMS T: {rmsT} , RMS Ca: {rmsCa})")

    plt.subplot(2,1,2)
    Cr_list_ = df.set_index('time')['Ca']
    Cref_list = df.set_index('time')['Cref'][:90]
    min_Cr = [min(np.array(Cr_list_[i])) for i in range(90)]
    max_Cr = [max(np.array(Cr_list_[i])) for i in range(90)]
    mean_Cr = [np.mean(np.array(Cr_list_[i])) for i in range(90)]
    plt.fill_between([i for i in range(90)] , min_Cr , max_Cr, alpha = 0.2)
    plt.plot([i for i in range(90)],Cref_list,'k--',lw=2,label=r'$C_{sp}$')
    plt.plot([i for i in range(90)],mean_Cr,'b.-',lw=1,label=r'$C_{sp}$')
    plt.ylabel('Concentration')

    plt.savefig('./cstr/linear_mpc/benchmark_figure.png')


if __name__ == "__main__":
    start()
