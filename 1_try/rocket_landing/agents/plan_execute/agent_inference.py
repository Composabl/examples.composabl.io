from asyncore import loop
import os
import sys
import asyncio
from typing import Protocol

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Trainer, Scenario
from composabl_core.networking.client import make
from config import config
from sensors import sensors
from scenarios import Navigation_scenarios, X_variation_scenarios
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from ipywidgets import IntProgress
import math
from mpc_actions import thrust_optm, angle_optm

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"
PATH_BENCHMARKS = f"{PATH}/benchmarks"

DELETE_OLD_HISTORY_FILES: bool = True

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

    #"Initializing Environment"
    print("Initializing Environment")
    await sim.init()
    print("Initialized")

    await sim.set_scenario(Scenario(X_variation_scenarios[0]))
    df = pd.DataFrame()
    obs_history = []
    thrust_history = []
    t = 0
    a = 0
    deg_to_rad = 0.01745329252
    max_gimble = 20 * deg_to_rad
    min_gimble = max_gimble
    #"Resetting Environment"
    obs, info = await sim.reset()
    obs_history.append(obs)

    for i in range(400):
        action = await trained_agent._execute(obs)
        print(action)
        #print( angle_optm[i],thrust_optm[i])
        print( thrust_optm[i], angle_optm[i])

        '''if i == 0:
            t = thrust_optm[i] - 0
            a = angle_optm[i] - 0
        else:
            t = thrust_optm[i] - thrust_optm[i-1]
            a = angle_optm[i] - angle_optm[i-1]

        action = [t, a]'''

        obs, reward, done, truncated, info = await sim.step(action)
        df_temp = pd.DataFrame(columns=[s.name for s in sensors] + ['time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        obs_history.append(obs)
        #t += action[1]
        #a += action[0]
        t = action[1]
        a = action[0]
        #t = np.clip(t,0.4,1)
        #a = np.clip(a, min_gimble, max_gimble)


        thrust_history.append([t, a])

        if done:
            break

    sim.close()
    print('###############')
    #print(thrust_optm)
    #print(angle_optm)
    print('###############')

    # save history data
    df.to_pickle(f"{PATH_HISTORY}/inference_data.pkl")

    # plot
    x = np.array(obs_history)
    u = np.array(thrust_history[:])
    length = 50 # m
    width = 10
    #steps = 400
    steps = len(x)

    t_step= 0.04
    final_time_step = t_step
    duration = t_step * steps

    #print("Generating Animation")
    f = IntProgress(min = 0, max = steps)
    #display(f)

    x_t = x
    u_t = u

    fig = plt.figure(figsize = (5, 5), constrained_layout=False)

    ax1 = fig.add_subplot(111)

    ln6, = ax1.plot([], [], '--', linewidth = 2, color = 'orange')

    ln2, = ax1.plot([], [], linewidth = 2, color = 'tomato')
    ln1, = ax1.plot([], [], linewidth = 5, color = 'lightblue')

    #plt.axis('off')
    plt.tight_layout()

    ax1.set_xlim(-400, 400)
    ax1.set_ylim(-50, 1000)
    ax1.set_aspect(1)

    def update(i):
        rocket_theta = x_t[i, 4]

        rocket_x = x_t[i, 0]
        rocket_x_points = [rocket_x + length/2 * math.sin(rocket_theta), rocket_x - length/2 * math.sin(rocket_theta)]

        rocket_y = x_t[i, 2]
        rocket_y_points = [rocket_y + length/2 * math.cos(rocket_theta), rocket_y - length/2 * math.cos(rocket_theta)]

        ln1.set_data(rocket_x_points, rocket_y_points)

        thrust_mag = u_t[i, 0]
        thrust_angle = -u_t[i, 1]

        flame_length = (thrust_mag) * 50

        flame_x_points = [rocket_x_points[1], rocket_x_points[1] + flame_length * math.sin(thrust_angle - rocket_theta)]
        flame_y_points = [rocket_y_points[1], rocket_y_points[1] - flame_length * math.cos(thrust_angle - rocket_theta)]

        ln2.set_data(flame_x_points, flame_y_points)

        ln6.set_data(x_t[:i, 0], x_t[:i, 2])

        f.value += 1

    anim = FuncAnimation(fig, update, np.arange(0, steps-1, 1), interval= final_time_step * 1000)

    plt.title("Rocket Landing")

    anim.save(f"{PATH_BENCHMARKS}/inference_figure.gif", writer='pillow')

    plt.show()
    plt.subplot(2,1,1)
    #print(thrust_history)
    #print([x[0] for x in thrust_history])
    plt.plot([x[0] for x in thrust_history])
    plt.plot(thrust_optm)
    #plt.plot([x[1] for x in thrust_history])

    plt.subplot(2,1,2)
    plt.plot([x[1] for x in thrust_history])
    plt.plot(angle_optm)
    plt.show()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_agent())
