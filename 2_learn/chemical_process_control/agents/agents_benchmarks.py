from asyncore import loop
import asyncio
import os

from composabl import Agent, Trainer, Scenario
from composabl_core.networking.client import make
from sensors import sensors
from config import config
from scenarios import reaction_scenarios, ss1_scenarios, ss2_scenarios, transition_scenarios, selector_scenarios
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

agents_folders = os.listdir(PATH)

# get only checkpoint folders and their names and store in one dict
agents = {}
for folder in agents_folders:
    # if is a folder
    if not os.path.isdir(f"{PATH}/{folder}"):
        continue

    for agent_folder in os.listdir(f"{PATH}/{folder}"):
        if agent_folder == "checkpoints":
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
    await sim.set_scenario(reaction_scenarios)
    obs_history = []
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

        if done:
            break

    print("Closing")
    await sim.close()

    # save history data
    #df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    #print(df)
    #plt.plot(df['time'], df['x'], label='x')
    plt.subplot(2, 1, 1)
    plt.plot(df['time'], df['Ca'])
    plt.ylabel('Concentration')

    plt.subplot(2, 1, 2)
    plt.plot(df['time'], df['T'])
    plt.ylabel('Temperature')





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

    #plt.ylim(-10, 1000)
    #plt.xlim(-500, 500)
    Cref = [8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.57, 8.443653846153847, 8.317307692307693, 8.190961538461538, 8.064615384615385, 7.938269230769231, 7.811923076923077, 7.6855769230769235, 7.559230769230769, 7.432884615384616, 7.306538461538461, 7.180192307692308, 7.053846153846154, 6.9275, 6.801153846153847, 6.674807692307692, 6.548461538461538, 6.422115384615385, 6.295769230769231, 6.169423076923077, 6.043076923076923, 5.916730769230769, 5.790384615384616, 5.664038461538461, 5.537692307692308, 5.411346153846154, 5.285, 5.158653846153847, 5.032307692307692, 4.905961538461538, 4.779615384615385, 4.653269230769231, 4.526923076923077, 4.400576923076923, 4.274230769230769, 4.147884615384616, 4.021538461538461, 3.895192307692308, 3.7688461538461535, 3.6425, 3.5161538461538457, 3.3898076923076923, 3.263461538461538, 3.1371153846153845, 3.01076923076923, 2.8844230769230768, 2.7580769230769224, 2.631730769230769, 2.5053846153846155, 2.379038461538461, 2.2526923076923078, 2.1263461538461534, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    Tref = [311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 311.2612, 312.45100576923073, 313.6408115384615, 314.8306173076923, 316.02042307692307, 317.2102288461538, 318.4000346153846, 319.58984038461534, 320.77964615384616, 321.9694519230769, 323.1592576923077, 324.34906346153844, 325.5388692307692, 326.72867499999995, 327.91848076923077, 329.1082865384615, 330.2980923076923, 331.48789807692305, 332.6777038461538, 333.8675096153846, 335.0573153846154, 336.24712115384614, 337.4369269230769, 338.62673269230766, 339.81653846153847, 341.00634423076923, 342.19615, 343.38595576923075, 344.5757615384615, 345.7655673076923, 346.9553730769231, 348.14517884615384, 349.3349846153846, 350.52479038461536, 351.7145961538462, 352.90440192307693, 354.0942076923077, 355.28401346153845, 356.4738192307692, 357.663625, 358.8534307692308, 360.04323653846154, 361.2330423076923, 362.42284807692306, 363.6126538461538, 364.80245961538463, 365.9922653846154, 367.18207115384615, 368.3718769230769, 369.56168269230767, 370.7514884615385, 371.94129423076924, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311, 373.1311]
    plt.subplot(2, 1, 1)
    plt.plot(Cref, linestyle='--')
    plt.title('Agent Benchmarks')
    plt.legend(legends)

    plt.subplot(2, 1, 2)
    plt.plot(Tref, linestyle='--')

    #plt.show()
    plt.savefig(f"{PATH}/benchmark_agents.png")


