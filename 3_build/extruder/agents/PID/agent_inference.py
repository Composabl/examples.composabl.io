import asyncio
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Trainer, Scenario, Sensor, Skill
from config import config
from sensors import sensors
from composabl_core.networking.client import make
import pandas as pd
import matplotlib.pyplot as plt

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/model"
PATH_BENCHMARKS = f"{PATH}/benchmarks"

DELETE_OLD_HISTORY_FILES: bool = True

async def start():
    # Start Runtime
    trainer = Trainer(config)

    # Load the pre trained agent
    agent = Agent.load(PATH_CHECKPOINTS)

    # Prepare the loaded agent for inference
    trained_agent = trainer.package(agent)

    # Inference
    #"Creating Environment"
    sim = make(
        run_id="run-benchmark",
        sim_id="sim-benchmark",
        env_id="sim",
        address="localhost:1337",
        env_init={},
        init_client=False,
        #protocol = Protocol
    )

    #"Initializing Environment"
    await sim.init()
    #"Initialized"
    await sim.set_scenario(Scenario({
            "y1ref": 170, #170
            "time_delay": 0.028
        }))
    df = pd.DataFrame()
    total_steps = 30
    #"Resetting Environment"
    obs, info = await sim.reset()

    for i in range(total_steps):
        action = await trained_agent._execute(obs, explore=False)
        print(action)
        #action = await sim.action_space_sample()
        obs, reward, done, truncated, info = await sim.step(action)

        df_temp = pd.DataFrame(columns= [s.name for s in sensors] + ['time', 'action'],data=[[float(x) for x in list(obs)] + [i, action]])
        df = pd.concat([df, df_temp])

        if done or truncated:
            print("BREAK")
            #break

    await sim.close()

    # save history data
    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    #df.reset_index().plot(subplots=True, figsize=(10,10))
    #plt.show()


    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(3,1,1)
    plt.plot(df.reset_index()['time'],df.reset_index()['y1'])
    plt.axhline(y= df.reset_index()['y1ref'][0], color='r', linestyle='--')
    #plt.ylabel('outside_temperature')
    plt.legend(['temperature'],loc='best')
    plt.title('Agent Inference')

    plt.subplot(3,1,2)
    plt.plot(df.reset_index()['time'],df.reset_index()['u1'])
    plt.ylabel('control')
    #plt.legend(['hvac_demo_room_flow', 'hvac1_demo_room_flow'],loc='best')

    plt.subplot(3,1,3)
    plt.plot(df.reset_index()['time'],df.reset_index()['rms'])
    #plt.plot(df.reset_index()['time'],df.reset_index()['Cref'],'r--')
    #plt.legend(['people_inside_demo_room', 'hvac_demo_room_on', 'temperature_mode'
    #            'hvac1_demo_room_on', 'manualHVACIsInUse'],loc='best')
    #plt.ylabel('Concentration')
    plt.xlabel('iteration')

    plt.savefig(f"{PATH_BENCHMARKS}/inference_figure.png")

    ####### RANDOM AGENT
    #"Resetting Environment"
    print("RUN RANDOM AGENT")
    df_ = pd.DataFrame()
    obs, info = await sim.reset()
    region = False
    for i in range(total_steps):
        #action = await trained_agent._execute(obs)
        action = await sim.action_space_sample()

        obs, reward, done, truncated, info = await sim.step(action[0])
        print(obs)

        df_temp_ = pd.DataFrame(columns= [s.name for s in sensors] + ['time', 'action'],data=[[float(x) for x in list(obs)] + [i, action]])
        df_ = pd.concat([df_, df_temp_])

        #if done or truncated:
        #    break

    await sim.close()

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(3,1,1)
    #plt.plot(df.reset_index()['time'],df.reset_index()['outside_temperature'])
    plt.plot(df.reset_index()['time'],df.reset_index()['y1'])
    plt.plot(df_.reset_index()['time'],df_.reset_index()['y1'])
    #plt.axhline(y=20, color='r', linestyle='--')
    #plt.axhline(y=19, color='g', linestyle='--')
    #plt.axhline(y=21, color='g', linestyle='--')
    #plt.legend(['model_temperature', 'random_temperature', 'plan execute'],loc='best')

    plt.subplot(3,1,2)
    plt.plot(df.reset_index()['time'],df.reset_index()['u1'])
    plt.plot(df_.reset_index()['time'],df_.reset_index()['u1'])
    plt.legend(['model_cost', 'random_cost', 'plan execute'],loc='best')

    #plt.subplot(3,1,3)
    #plt.plot(df.reset_index()['time'],df.reset_index()['outside_temperature'])
    #plt.legend(['outside_temperature'],loc='best')


    plt.savefig(f"{PATH_BENCHMARKS}/benchmark_figure.png")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
