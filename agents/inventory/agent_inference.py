import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import BalanceTeacher

from external_sim.sim import Env
import pandas as pd
import matplotlib.pyplot as plt
import random

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def start():
    Q1_scenarios = [
        {
            "holding_cost": 2,
            "cost_price": 20,
            "delay_days_until_delivery": 5,
            "customer_demand_min": 1,
            "customer_demand_max": 3,
            "selling_price": 25,
            "run_time": 60
        }
    ]

    Balance_skill = Skill("Balance", BalanceTeacher, trainable=True)

    for scenario_dict in Q1_scenarios:
        scenario = Scenario(scenario_dict)
        Balance_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            #"docker": {
            #    "image": "composabl/sim-inventory-management"
            #},
            "local": {
                "address": "localhost:1337"
            }

        },
        "env": {
            "name": "inventory-management",
        },
        "training": {}
    }

    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(Balance_skill)

    files = os.listdir(PATH_CHECKPOINTS)
    if '.DS_Store' in files:
        files.remove('.DS_Store')

    if len(files) > 0:
        #load agent
        agent.load(PATH_CHECKPOINTS)

    #save agent
    trained_agent = agent.prepare()

    # Inference
    sim = Env()
    sim.scenario = Scenario({
            "holding_cost": 2,
            "cost_price": 20,
            "delay_days_until_delivery": 5,
            "customer_demand_min": 1,
            "customer_demand_max": 3,
            "selling_price": 25,
            "run_time": 30
        })
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(30):
        action = trained_agent.execute(obs)
        action = action[0]
        action = [action*1 for i in action]
        obs, reward, done, truncated, info = sim.step(action[0])

        df_temp = pd.DataFrame(columns=['inventory','balance','num_ordered','order_cutoff','order_target','time'],
        data=[[obs[0],obs[1],obs[2],action[0][0], action[0][1],i]])
        df = pd.concat([df, df_temp])

        if done:
            break

    # save history data
    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(4,1,1)
    plt.plot(df.reset_index()['time'],df.reset_index()['inventory'])
    plt.ylabel("Inventory level")
    plt.title(f"Final Balance {round(df['balance'].to_list()[-1],1)} $" )

    plt.subplot(4,1,2)
    plt.plot(df.reset_index()['time'],df.reset_index()['balance'])
    plt.ylabel("Balance History ($)")


    plt.subplot(4,1,3)
    plt.plot(df.reset_index()['time'],df.reset_index()['order_cutoff'])
    plt.ylabel('order_cutoff')


    plt.subplot(4,1,4)
    plt.plot(df.reset_index()['time'],df.reset_index()['order_target'])
    plt.ylabel('order_target')
    plt.xlabel("Simulation time (days)")


    print(f"Final Balance {df['balance'].to_list()[-1]} Total Balance {df['balance'].sum()}" )


    plt.savefig(f"{PATH}/inference_figure.png")

if __name__ == "__main__":
    start()
