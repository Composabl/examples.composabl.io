from asyncore import loop
import os
import sys
import asyncio
from typing import Protocol

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Trainer, Scenario
from composabl_core.networking.client import make
from sensors import sensors
from config import config
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"
PATH_BENCHMARKS = f"{PATH}/benchmarks"

async def run_agent():
    # Start Runtime
    trainer = Trainer(config)

    # Load the pre trained agent
    agent = Agent.load(PATH_CHECKPOINTS)

    # Prepare the loaded agent for inference
    trained_agent = await trainer._package(agent)

    # Inference
    print("Creating Environment")
    sim = make(
        run_id="run-benchmark",
        sim_id="sim-benchmark",
        env_id="sim",
        address="localhost:1337",
        env_init={},
        init_client=False,
        #protocol = Protocol
    )

    print("Initializing Environment")
    await sim.init()
    print("Initialized")

    # Set scenario
    noise = 0.0
    await sim.set_scenario(Scenario({
            "Cref_signal": "complete",
            "noise_percentage": noise
        }))

    obs_history = []
    df = pd.DataFrame()
    print("Resetting Environment")
    obs, info = await sim.reset()
    obs_history.append(obs)
    for i in range(89):
        action = await trained_agent._execute(obs)
        obs, reward, done, truncated, info = await sim.step(action)
        df_temp = pd.DataFrame(columns=[s.name for s in sensors] + ['time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        obs_history.append(obs)

        if done:
            break

    print("Closing")
    await sim.close()

    # save history data
    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(3,1,1)
    plt.plot(df.reset_index()['time'],df.reset_index()['Tc'])
    plt.ylabel('Tc')
    plt.legend(['reward'],loc='best')
    plt.title('Agent Inference DRL' + f" - Noise: {noise}")

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
