import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Scenario
from sensors import sensors
from composabl_core.grpc.client.client import make
import numpy as np
import matplotlib.pyplot as plt
import pickle
from order_controller import OrderController

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

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

    cont = OrderController()
    last_reward_history_total = []
    for j in range(30):
        print(f'Run {j}')
        total_reward_history = []
        last_reward_history = []
        last_revenue_history = []
        production_history = []
        demand_history = []

        for d in range(7):
            cont.reset()
            co_dm = scenarios_list[d]['co_dm']
            cp_dm = scenarios_list[d]['cp_dm']
            ck_dm = scenarios_list[d]['ck_dm']
            metrics = {
                'Co_demand': co_dm,
                'Cp_demand': cp_dm,
                'Ck_demand': ck_dm
            }

            sim.init()

            sim.set_scenario(Scenario({
                    "cookies_demand": co_dm,
                    "cupcake_demand": cp_dm,
                    "cake_demand": ck_dm,
                }))

            obs, info = sim.reset()
            demand_history.append([co_dm, cp_dm, ck_dm])

            # Get a sim action sample if needed (debug)
            obs_history = []
            action_history = []
            reward_history = []

            sensors_name = [s.name for s in sensors]
            obs_base = {}

            for s in sensors_name:
                obs_base[s] = None

            for i in range(480):
                # Extract agent actions - Here you can pass the obs (observation state), call the agent.execute() and get the action back
                action = cont.compute_action(obs)
                action_history.append(action)

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

                old_obs = obs.copy()
                obs = dict(map(lambda i,j : (i,j), sensors_name, obs))
                obs_history.append(obs)
                ccok = obs['completed_cookies']
                ccup = obs['completed_cupcakes']
                ccak = obs['completed_cake']
                revenue = ccok * float(obs['cookies_price']) + ccup * float(obs['cupcake_price']) + ccak * float(obs['cake_price'])

                obs = old_obs

                if done:
                    break

            metrics['completed_cookies'] = ccok
            metrics['completed_cupcakes'] = ccup
            metrics['completed_cake'] = ccak

            #print('Day: ', d, ' metrics:', metrics)

            total_reward_history.append(reward_history)
            last_reward_history.append(sim_reward)
            last_revenue_history.append(revenue)
            production_history.append([ccok, ccup, ccak])

            sim.close()

        last_reward_history_total.append(last_reward_history)

    # Plot the results
    min_reward = [min(np.array(last_reward_history_total)[:,i]) for i in range(7)]
    max_reward = [max(np.array(last_reward_history_total)[:,i])for i in range(7)]
    mean_reward = [np.mean((np.array(last_reward_history_total)[:,i])) for i in range(7)]
    std_reward = [np.std((np.array(last_reward_history_total)[:,i])) for i in range(7)]

    #profit Margin
    profit_margin = [ (mean_reward[i]/last_revenue_history[i])*100 for i in range(7)]

    with open('metrics.pkl', 'wb') as f:
        pickle.dump(metrics, f)

    #print("Done", ccok, ccup, ccak)

    plt.figure(4,figsize=(10,7))
    x = np.arange(len(last_revenue_history))
    plt.subplot(4,1,1)
    #plt.plot(last_reward_history,'k.-',lw=2)
    plt.plot(mean_reward,'k.-',lw=2)
    plt.fill_between([i for i in range(7)] , min_reward , max_reward, alpha = 0.2)
    plt.axhline(y=0, color='k', linestyle='--')
    plt.ylabel('Profit')
    plt.xticks(x, ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    plt.legend(['mean_profit','std_profit'],loc='best')

    plt.title(f'Total Profit {round(sum(min_reward),2)} < {round(sum(mean_reward),2)} < {round(sum(max_reward),2)} | Total Revenue {round(sum(last_revenue_history),2)} | Profit Margin {round(np.mean(profit_margin),0)} % | Adapt Index {round(100/np.mean(std_reward),2)}')

    plt.subplot(4,1,2)
    plt.plot(last_revenue_history,'k.-',lw=2)
    plt.ylabel('Revenue')
    plt.xticks(x, ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

    plt.subplot(4,1,3)
    plt.plot(profit_margin,'r.-',lw=2)
    plt.axhline(y=0, color='k', linestyle='--')
    plt.ylabel('Profit Margin')
    plt.xticks(x, ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

    plt.subplot(4,1,4)
    #plt.bar(['cookies','cupcakes', 'cakes'], [float(ccok), float(ccup), float(ccak)])
    w = 0.35
    #plt.bar( np.arange(len(last_revenue_history)) , [tuple(x) for x in production_history] )
    plt.bar( x - w/3, [x[0] for x in production_history], w/3)
    plt.bar( x  , [x[1] for x in production_history], w/3 )
    plt.bar( x + w/3 , [x[2] for x in production_history], w/3 )
    plt.plot([ x[0] for x in demand_history], 'b--')
    plt.plot([ x[1] for x in demand_history], 'r--')
    plt.plot([ x[2] for x in demand_history], 'g--')
    plt.ylabel('Demand and Production')
    plt.legend(['cookies','cupcakes', 'cakes'])
    plt.xticks(x, ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    plt.xlabel('Day of the week')

    plt.savefig(f"{PATH}/img/benchmarks.png")


if __name__ == "__main__":
    run_agent()

