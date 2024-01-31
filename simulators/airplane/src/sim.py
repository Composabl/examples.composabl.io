from typing import Any, Dict, SupportsFloat, Tuple, Optional
import math
import random
import numpy as np

import control
from scipy import signal

from composabl_core.agent.scenario import Scenario
import gymnasium as gym


class AirplaneEnv(gym.Env):
    def __init__(self):
        '''
        actions = 2 :
            de: elevator angle variation
            dt: thrust variation
        observation_variables = 6 :
            y1: Air Speed
            y1: Climb Rate
            u1: horizontal velocity
            u2: vertical velocity
            u3: rotation
            u4: angle

        '''
        obs_space = {"y1": {"low": -200, "high": 200},
                     "y2": {"low": -200, "high": 200},
                     "u1": {"low": -1000.0, "high": 1000.0},
                     "u2": {"low": -1000.0, "high": 1000.0},
                     "u3": {"low": -1000.0, "high": 1000.0},
                     "u4": {"low": -1000.0, "high": 1000.0}
                     }


        low_list = [x['low'] for x in obs_space.values()]
        high_list = [x['high'] for x in obs_space.values()]

        self.observation_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        action_space = {"de": {"low": -1.0, "high": 1.0},
                        "dt": {"low": -1.0, "high": 1.0}
                        }

        low_act_list = [x['low'] for x in action_space.values()]
        high_act_list = [x['high'] for x in action_space.values()]

        self.action_space = gym.spaces.Box(low=np.array(low_act_list), high=np.array(high_act_list))

        # initial conditions
        self.y1 = 0
        self.y2 = 0
        self.u1 = 0
        self.u2 = 0
        self.u3 = 0
        self.u4 = 0
        self.scenario = None

    def reset(self):
        self.done = False

        # Define scenario in the simulation
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])

        self.e = 0
        self.t = 0
        self.ulist = [[0, 0]]

        self.de = 0
        self.dt = 0

        self.cnt = 1
        self.rms = 1

        # initialize plant model
        self.time_max = 0

        self.y1_list = []
        self.dt = 1
        self.I = 0
        uw = random.uniform(14.67, 58.67) / 100
        vw = random.uniform(14.67, 58.67) / 100

        uw = 0  # no variation
        vw = 0  # no variation

        A = np.array([[-.003 * (1 - uw), 0.039 * (1 - vw), 0, -0.322],
                      [-0.065 * (1 - uw), -0.319 * (1 - vw), 7.74, 0],
                      [0.020 * (1 - uw), -0.101 * (1 - vw), -0.429, 0],
                      [0, 0, 1, 0]])

        B = np.array([[0.01, 1],
                      [-0.18, -0.04],
                      [-1.16, 0.598],
                      [0, 0]])

        C = np.array([[1, 0, 0, 0],
                      [0, -1, 0, 7.74]])

        D = np.array([[0, 0],
                      [0, 0]
                      ])

        dt = 0  # sample time, 0 = continuous, >0 = discrete
        #self.sys = control.StateSpace(A, B, C, D)
        self.sys1 = signal.StateSpace(A, B, C, D)

        self.cnt = 0

        self.obs = {"y1": self.y1,
                    "y2": self.y2,
                    "u1": self.u1,
                    "u2": self.u2,
                    "u3": self.u3,
                    "u4": self.u4
                   }

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, info

    def step(self, action):
        if len(action) == 0:
            de = 0
            dt = 0
        else:
            de = action[0]  # de
            dt = action[1]  # dt

        self.de = de
        self.dt = dt

        self.e += de
        self.t += dt

        u = np.array([1, 1])

        #io = control.ss2io(self.sys)

        tm = np.linspace(0, self.cnt, self.cnt + 1)  # 1 sec

        # clip u from -5 to 5
        self.e = np.clip(self.e, -5, 5)
        self.t = np.clip(self.t, -5, 5)

        # add u into the list
        if self.cnt == 0:
            self.u_list = u
        else:
            self.ulist.append([self.e, self.t])

        t, yout, xout = signal.lsim(self.sys1, self.ulist, tm)

        if len(np.array(yout).shape) <= 1:
            yout = [yout]
            xout = [xout]

        ix = -1

        self.y1 = yout[ix][0]
        self.y2 = yout[ix][1]

        self.u1 = xout[ix][0]
        self.u2 = xout[ix][1]
        self.u3 = xout[ix][2]
        self.u4 = xout[ix][3]

        # update env obs
        self.obs = {"y1": self.y1,
                    "y2": self.y2,
                    "u1": self.u1,
                    "u2": self.u2,
                    "u3": self.u3,
                    "u4": self.u4
                    }
        self.obs = np.array(list(self.obs.values()))


        self.e1 = 0.001 if (-9.5 < self.y1 < -8.5) else abs(self.y1 - ((-9.5 + -8.5) / 2))  # (-9.5,-8.5)
        self.e2 = 0.001 if (4.6 < self.y2 < 5.4) else abs(self.y2 - ((4.6 + 5.4) / 2))  # (4.6,5.4)

        # Increase time
        self.cnt += 1

        # reward = env reward, self.reward = custom reward
        self.reward = float(1 / (self.e1 + self.e2))

        # end the simulation
        done = self.done
        # print(done)
        if self.cnt > 16:
            done = True

        info = {}
        return self.obs, self.reward, done, False, info

    def render(self, mode='human', close=False):
        print("render")
