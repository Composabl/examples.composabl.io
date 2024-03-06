import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors

from composabl_core.grpc.client.client import make
import numpy as np
import math
from gymnasium import spaces
import matplotlib.pyplot as plt
import pickle

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def start():
    # Define the right configuration
    config = {
        "license": license_key,
        "target": {
            #"docker": {
            #    "image": "composabl/sim-cstr:latest"
            #},
            "local": {
               "address": "localhost:1337"
            }
        },
        "env": {
            "name": "sim-whisky",
        },
        "runtime": {
            "workers": 1
        }
    }

    # Remove unused files from path (mac only)
    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    # Start Runtime
    runtime = Runtime(config)
    directory = PATH_CHECKPOINTS

    # Load the pre trained agent
    agent = Agent.load(directory)

    # Prepare the loaded agent for inference
    trained_agent = runtime.package(agent)
    
    # Create a new Simulation Environment
    print("Creating Environment")
    sim = make(
        "run-benchmark",
        "sim-benchmark",
        "",
        "localhost:1337",
        {
            "render_mode": "rgb_array",
            #"observation_space": _create_observation_space(),
            #"action_space": _create_action_space()
        },
    )

    print("Initializing Environment")
    sim.init()

    scenarios_list = [
        {'co_dm' : 100,
        'cp_dm' : 18,
        'ck_dm' : 5},
        {'co_dm' : 50,
        'cp_dm' : 10,
        'ck_dm' : 2},
        {'co_dm' : 200,
        'cp_dm' : 18,
        'ck_dm' : 3},
        {'co_dm' : 120,
        'cp_dm' : 18,
        'ck_dm' : 3},
        {'co_dm' : 120,
        'cp_dm' : 18,
        'ck_dm' : 2},
        {'co_dm' : 100,
        'cp_dm' : 42,
        'ck_dm' : 5},
        {'co_dm' : 50,
        'cp_dm' : 20,
        'ck_dm' : 10}
    ]

    total_reward_history = []
    last_reward_history = []

    for d in range(7):
        co_dm = scenarios_list[d]['co_dm']
        cp_dm = scenarios_list[d]['cp_dm']
        ck_dm = scenarios_list[d]['ck_dm']
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
        #a = sim.action_space_sample()
        obs_history = []
        action_history = []
        reward_history = []
        sensors_name = [s.name for s in sensors]
        obs_base = {}
        
        for s in sensors_name:
            obs_base[s] = None
        
        for i in range(480):
            # Extract agent actions - Here you can pass the obs (observation state), call the agent.execute() and get the action back
            action = trained_agent.execute(obs)
            action_history.append(action)
            #action = [action]
            #action = sim.action_space_sample()[0]

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
            
            #if done:
            #    break

        metrics['completed_cookies'] = ccok
        metrics['completed_cupcakes'] = ccup
        metrics['completed_cake'] = ccak

        print('Day: ', d, ' metrics:', metrics)

        total_reward_history.append(reward_history)
        last_reward_history.append(sim_reward)


    print('REWARD: ', last_reward_history)
    with open('metrics.pkl', 'wb') as f:
        pickle.dump(metrics, f)

    print("Done", ccok, ccup, ccak)
    print("Closing")
    sim.close()

    plt.figure(2,figsize=(10,7))
    plt.subplot(2,1,1)
    plt.plot(last_reward_history,'k.-',lw=2)
    plt.axhline(y=0, color='k', linestyle='--')
    plt.ylabel('Completed')
    plt.legend(['cookies','cupcakes','cake'],loc='best')
    plt.title('Live Control')

    plt.subplot(2,1,2)
    

    plt.xlabel('Time (min)')

    plt.savefig(f"{PATH}/img/benchmarks.png")
    

if __name__ == "__main__":
    start()

