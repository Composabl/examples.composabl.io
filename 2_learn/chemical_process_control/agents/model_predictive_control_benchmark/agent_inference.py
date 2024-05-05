import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import matplotlib.pyplot as plt
import pandas as pd
from composabl import Agent, Scenario, Skill, Trainer
from composabl_core.grpc.client.client import make
from config import config
from controller import MPCController
from scenarios import reaction_scenarios
from sensors import sensors

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"
PATH_BENCHMARKS = f"{PATH}/benchmarks"

async def run_agent():
    reaction_skill = Skill("reaction", MPCController)
    for scenario_dict in reaction_scenarios:
        reaction_skill.add_scenario(Scenario(scenario_dict))

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    # Inference
    noise = 0.0
    cont = MPCController()
    sim = make(
        "run-benchmark",
        "sim-benchmark",
        "",
        "localhost:1337",
        {
            "render_mode": "rgb_array"
        },
    )
    sim.init()
    sim.set_scenario(Scenario({
            "Cref_signal": "complete",
            "noise_percentage": noise
        }))
    df = pd.DataFrame()
    obs, info = sim.reset()

    for i in range(90-1):
        action = cont.compute_action(obs)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break

    sim.close()
    # save history data
    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(3,1,1)
    plt.plot(df.reset_index()['time'],df.reset_index()['Tc'])
    plt.ylabel('Tc')
    plt.legend(['reward'],loc='best')
    plt.title('Agent Inference Linear MPC' + f" - Noise: {noise}")

    plt.subplot(3,1,2)
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

    plt.savefig(f"{PATH_BENCHMARKS}/inference_figure.png")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_agent())
