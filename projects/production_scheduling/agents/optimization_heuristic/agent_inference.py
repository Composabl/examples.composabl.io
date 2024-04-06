import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors

from composabl_core.grpc.client.client import make
import numpy as np
import math
from gymnasium import spaces
import matplotlib.pyplot as plt
import pickle
from heuristic_controller import OrderController

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

## INFERENCE FOR HEURISTIC CONTROLLER

def run_agent():
    # Create a new Simulation Environment
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
    co_dm = 100
    cp_dm = 18
    ck_dm = 5
    metrics = {
        'Co_demand': co_dm,
        'Cp_demand': cp_dm,
        'Ck_demand':ck_dm
    }

    sim.set_scenario(Scenario({
            "cookies_demand": co_dm,
            "cupcake_demand": cp_dm,
            "cake_demand": ck_dm,
        }))
    print("Resetting Environment")
    obs, info = sim.reset()
    print("Initialized")
    # Get a sim action sample if needed (debug)
    obs_history = []
    action_history = []
    reward_history = []
    sensors_name = [s.name for s in sensors]
    obs_base = {}
    cont = OrderController()

    for s in sensors_name:
        obs_base[s] = None

    for i in range(480):
        # Extract agent actions - Here you can pass the obs (observation state), call the agent.execute() and get the action back
        action = cont.compute_action(obs)

        obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
        obs_history.append(obs)
        ccok = obs['completed_cookies']
        ccup = obs['completed_cupcakes']
        ccak = obs['completed_cake']

        observation_dict = {
            0:'sim_time',
            1:'baker_1_time_remaining',
            2:'baker_2_time_remaining',
            3:'baker_3_time_remaining',
            4:'baker_4_time_remaining',
            # EQUIPMENT
            5:'mixer_1_recipe',
            6:'mixer_1_time_remaining',
            7:'mixer_2_recipe',
            8:'mixer_2_time_remaining',
            9:'oven_1_recipe',
            10:'oven_1_time_remaining',
            11:'oven_2_recipe',
            12:'oven_2_time_remaining',
            13:'oven_3_recipe',
            14:'oven_3_time_remaining',
            15:'decorating_station_1_recipe',
            16:'decorating_station_1_time_remaining',
            17:'decorating_station_2_recipe',
            18:'decorating_station_2_time_remaining',
            # DESSERT CASE
            #19:'completed_cookies',
            #20:'completed_cupcakes',
            #21:'completed_cake',
        }

        obs, sim_reward, done, terminated, info =  sim.step(action)
        reward_history.append(sim_reward)

        if done:
            break

    metrics['completed_cookies'] = ccok
    metrics['completed_cupcakes'] = ccup
    metrics['completed_cake'] = ccak

    with open('history/metrics.pkl', 'wb') as f:
        pickle.dump(metrics, f)

    print("Done", ccok, ccup, ccak)
    print("Closing")
    sim.close()

    plt.figure(2,figsize=(7,5))
    plt.subplot(4,1,1)
    plt.plot([ x["completed_cookies"] for x in obs_history],'k.-',lw=2)
    plt.plot([ x["completed_cupcakes"] for x in obs_history],'b.-',lw=2)
    plt.plot([ x["completed_cake"] for x in obs_history],'r.-',lw=2)
    plt.ylabel('Completed')
    plt.legend(['cookies','cupcakes','cake'],loc='best')
    plt.title('Live Control')

    plt.subplot(4,1,2)
    '''plt.bar(['cookies','cupcakes', 'cakes'], [float(obs_history[-1]["completed_cookies"]),
                                                float(obs_history[-1]["completed_cupcakes"]),
                                                float(obs_history[-1]["completed_cake"])
                                                ])'''
    plt.plot([ x[observation_dict[5]] for x in obs_history],'k.-',lw=2)
    plt.plot([ x[observation_dict[6]] for x in obs_history],'k.-',lw=2)
    plt.plot([ x[observation_dict[9]] for x in obs_history],'r.-',lw=2)
    plt.plot([ x[observation_dict[10]] for x in obs_history],'r.-',lw=2)
    plt.plot([ x[observation_dict[15]] for x in obs_history],'g.-',lw=2)
    plt.plot([ x[observation_dict[16]] for x in obs_history],'g.-',lw=2)
    plt.ylabel('Completed')
    plt.legend(['cookies','cupcakes','cake', 'completed'],loc='best')

    plt.subplot(4,1,3)
    plt.plot(action_history)
    plt.ylabel('Income')
    plt.legend(['cookie','cupcake','cake'],loc='best')

    plt.subplot(4,1,4)
    plt.plot(reward_history,'k--',lw=2,label=r'$T_{sp}$')
    plt.ylabel('Reward')
    plt.xlabel('Time (min)')
    plt.legend(['Reward'],loc='best')

    plt.savefig(f"{PATH}/img/inference_figure_heuristic.png")


if __name__ == "__main__":
    run_agent()

