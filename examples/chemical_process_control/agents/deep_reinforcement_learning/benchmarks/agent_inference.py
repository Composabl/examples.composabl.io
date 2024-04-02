import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill

#from composabl_core.grpc.client.client import make
from composabl_core.networking.client import make
#from composabl_core.networking import server as make
from sensors import sensors
from config import config
import pandas as pd
import matplotlib.pyplot as plt

#from utils.cleanup import cleanup_folder
#from utils.config import generate_config
#print('PATH: ', os.path.join(os.path.dirname(__file__), "..", "checkpoints"))
PATH = os.path.dirname(os.path.realpath(__file__))
#PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = os.path.join(os.path.dirname(__file__), "..", "checkpoints")

DELETE_OLD_HISTORY_FILES: bool = True

async def start():
    # Start Runtime
    runtime = Runtime(config)

    # Load the pre trained agent
    #cleanup_folder(PATH_CHECKPOINTS, ".DS_Store")
    agent = Agent.load(PATH_CHECKPOINTS)

    # Prepare the loaded agent for inference
    trained_agent = await runtime.package(agent)

    # Inference
    print("Creating Environment")
    sim = make(
        "run-benchmark",
        "sim-benchmark",
        "",
        "localhost:1337",
        {
            "render_mode": "rgb_array",
        },
    )

    print("Initializing Environment")
    sim.init()
    print("Initialized")

    noise = 0.0
    sim.set_scenario(Scenario({
            "Cref_signal": "complete",
            "noise_percentage": noise
        }))
    df = pd.DataFrame()
    print("Resetting Environment")
    obs, info = await sim.reset()
    for i in range(90):
        action = await trained_agent.execute(obs)
        obs, reward, done, truncated, info = await sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break

    print("Closing")
    await sim.close()

    # save history data
    #df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

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

    plt.savefig(f"{PATH}/img/inference_figure.png")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
