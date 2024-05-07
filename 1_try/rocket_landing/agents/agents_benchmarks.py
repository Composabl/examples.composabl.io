from asyncore import loop
import asyncio
import os

from composabl import Agent, Trainer, Scenario
from composabl_core.networking.client import make
from sensors import sensors
from config import config
from scenarios import Navigation_scenarios
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

#agents = os.listdir(PATH_CHECKPOINTS)

agents_folders = os.listdir(PATH)

# get only checkpoint folders and their names and store in one dict
agents = {}
for folder in agents_folders:
    # if is a folder
    if not os.path.isdir(f"{PATH}/{folder}"):
        continue

    for agent_folder in os.listdir(f"{PATH}/{folder}"):
        if agent_folder == "checkpoints":
            #agents[folder] = os.listdir(f"{PATH}/{folder}/{agent_folder}")
            agents[folder] = {}
            agents[folder]['checkpoints'] = f"{PATH}/{folder}/{agent_folder}"
            agents[folder]['teacher'] = f"{PATH}/{folder}/teacher.py"
            agents[folder]['controller'] = f"{PATH}/{folder}/controller.py"




async def run_agent(PATH_CHECKPOINTS):
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
    await sim.set_scenario(Navigation_scenarios)
    obs_history = []
    thrust_history = []
    t = 0
    a = 0
    df = pd.DataFrame()
    print("Resetting Environment")
    obs, info = await sim.reset()
    obs_history.append(obs)
    for i in range(400):
        action = await trained_agent._execute(obs)
        obs, reward, done, truncated, info = await sim.step(action)
        df_temp = pd.DataFrame(columns=[s.name for s in sensors] + ['time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        obs_history.append(obs)

        a = action[0]
        t = action[1]

        t = np.clip(t,0.4,1)
        a = np.clip(a, -3.15, 3.15)
        thrust_history.append([t, a])

        if done:
            break

    print("Closing")
    await sim.close()

    # save history data
    #df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    #print(df)
    #plt.plot(df['time'], df['x'], label='x')
    plt.plot(df['x'], df['y'])




if __name__ == "__main__":
    legends = []
    for agent in agents:
        print('#######################')
        print('LOADING AGENT: ', agent)
        PATH_CHECKPOINTS = agents[agent]['checkpoints']

        #copy teacher file to running folder
        teacher = agents[agent]['teacher']
        os.system(f"cp {teacher} {PATH}/teacher.py")

        #check for controller and import it
        if os.path.exists(agents[agent]['controller']):
            controller = agents[agent]['controller']
            os.system(f"cp {controller} {PATH}/controller.py")

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_agent(PATH_CHECKPOINTS))
            legends.append(agent)

            #remove teacher file
            os.system(f"rm {PATH}/teacher.py")
            os.system(f"rm {PATH}/controller.py")
        except Exception as e:
            print(e)
            continue



    plt.ylim(-10, 1000)
    plt.xlim(-500, 500)
    plt.title('Agent Benchmarks')
    plt.legend(legends)
    #plt.show()
    plt.savefig(f"{PATH}/benchmark_agents.png")


