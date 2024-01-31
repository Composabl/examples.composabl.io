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
            "delay_days_until_delivery": 40,
            "customer_demand_min": 1,
            "customer_demand_max": 3,
            "selling_price": 25,
            "run_time": 180
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
    scenario_dict = {
            "holding_cost": 2,
            "cost_price": 50,
            "selling_price": 100,
            'customer_demand_min':124,
            'customer_demand_max':174,
            "run_time": 180
        }
    sim = Env()
    sim.scenario = Scenario(scenario_dict)
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(10): # 5 years
        action = trained_agent.execute(obs)
        action = action[0]
        action = [action*4000 for i in action]
        #print(action[0])
        obs, reward, done, truncated, info = sim.step(action)

        df_temp = pd.DataFrame(columns=['inventory','balance','num_ordered','order_cutoff','time'],
        data=[[obs[0],obs[1],obs[2],action[0],i]])
        df = pd.concat([df, df_temp])

        #if done:
        #    break

    # save history data
    df['Storage Cost per Item'] = scenario_dict['holding_cost']
    df['Daily Demand Min'] = scenario_dict['customer_demand_min']
    df['Daily Demand Max'] = scenario_dict['customer_demand_max']
    df['Safety Stock'] = df['order_cutoff']
    df['Revenue'] = df['balance']
    df['Days'] = [scenario_dict["run_time"]*(i+1) for i in range(len(df))]

    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")
    df.to_csv(f"{PATH_HISTORY}/inference_data.csv")

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(4,1,1)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['inventory'])
    plt.ylabel("Inventory level")
    plt.title(f"Final Balance {round(df['balance'].to_list()[-1],1)} $" )

    plt.subplot(4,1,2)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['balance'])
    plt.ylabel("Balance History ($)")


    plt.subplot(4,1,3)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['order_cutoff'])
    plt.ylabel('order_cutoff')


    '''plt.subplot(4,1,4)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['order_target'])
    plt.ylabel('order_target')'''
    plt.xlabel("Simulation time (days)")


    print(f"Final Balance {df['balance'].to_list()[-1]} Total Balance {df['balance'].sum()}" )


    plt.savefig(f"{PATH}/inference_figure.png")

    # Inference Benchmark
    sim = Env()
    sim.scenario = Scenario({
            "holding_cost": 2,
            "cost_price": 20,
            "selling_price": 100,
            "run_time": 180
        })
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(10):
        action = [271]
        obs, reward, done, truncated, info = sim.step(action)

        df_temp = pd.DataFrame(columns=['inventory','balance','num_ordered','order_cutoff','time'],
        data=[[obs[0],obs[1],obs[2],action[0],i]])
        df = pd.concat([df, df_temp])

        #if done:
        #    break

    # save history data
    df['Storage Cost per Item'] = scenario_dict['holding_cost']
    df['Daily Demand Min'] = scenario_dict['customer_demand_min']
    df['Daily Demand Max'] = scenario_dict['customer_demand_max']
    df['Safety Stock'] = df['order_cutoff']
    df['Revenue'] = df['balance']
    df['Days'] = [scenario_dict["run_time"]*(i+1) for i in range(len(df))]

    df.to_pickle(f"{PATH_HISTORY}/inference_data_baseline.pkl")
    df.to_csv(f"{PATH_HISTORY}/inference_data_baseline.csv")

    # plot
    plt.figure(figsize=(10,5))
    plt.subplot(4,1,1)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['inventory'])
    plt.ylabel("Inventory level")
    plt.title(f"Final Balance {round(df['balance'].to_list()[-1],1)} $" )

    plt.subplot(4,1,2)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['balance'])
    plt.ylabel("Balance History ($)")


    plt.subplot(4,1,3)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['order_cutoff'])
    plt.ylabel('order_cutoff')


    '''plt.subplot(4,1,4)
    plt.plot([scenario_dict["run_time"]*(i+1) for i in range(len(df))],df.reset_index()['order_target'])
    plt.ylabel('order_target')'''
    plt.xlabel("Simulation time (days)")


    print(f"Baseline: Final Balance {df['balance'].to_list()[-1]} Total Balance {df['balance'].sum()}" )


    plt.savefig(f"{PATH}/inference_baseline_figure.png")

if __name__ == "__main__":
    start()
