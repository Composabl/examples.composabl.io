from typing import Any, Dict, SupportsFloat, Tuple, Optional
import numpy as np
import random

import control
import math

from composabl_core.agent.scenario import Scenario

import gymnasium as gym


class Env(gym.Env):
    def __init__(self):
        self.obs_space_constraints = {
            "y1": {'low': 0, 'high': 400},
            "y1ref": {'low': 0, 'high': 400},
            "u1": {'low': -120, 'high': 120},
            "rms": {'low': 0, 'high': 1000}
        }

        self.action_constraints = {
            #"du1": {'low': -40, 'high': 40},
            "du1": {'low': -200, 'high': 200},
        }

        low_list = [x['low'] for x in self.obs_space_constraints.values()]
        high_list = [x['high'] for x in self.obs_space_constraints.values()]

        self.observation_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        low_act_list = [x['low'] for x in self.action_constraints.values()]
        high_act_list = [x['high'] for x in self.action_constraints.values()]

        self.action_space = gym.spaces.Box(low=np.array(low_act_list), high=np.array(high_act_list))

        self.state_models = {}
        self.reward_models = {}
        self.scenario: Scenario = None

        self.time_delay = 0.028
        self.y1ref = 170
        self.noise_percentage = 0

    # Build the plant model from transfer functions
    # time step (seconds) between state updates
    Δt = 1
    def plant(self, i, j):
        num = [[[1.68]]
            ]
        den = [[[2.97, 1]]
            ]

        dt = 0  # sample time, 0 = continuous, >0 = discrete
        sys1 = control.tf(num[i - 1][j - 1], den[i - 1][j - 1], dt=dt)

        return sys1

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            options: Optional[dict] = None,
            noise_percentage: float = 0,
            y1_SP: float = 170,
            time_delay: float = 0.028
    ):
        '''
        obs[0] = y1 (extruder temperature)
        obs[1] = y1ref (extruder temperature SetPoint)
        obs[2] = "u1"
        obs[3]  = "rms" error

        time_delay (min) time delay
        noise_percentage :  actuator noise to add into the system
        '''
        #super().reset(seed=seed)
        self.cnt = 0

        # Define scenario in the simulation ******
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])
        #else:
        #    self.y1ref = 170
        #    self.time_delay = 0.028
        #    self.noise_percentage = 0

        # initial conditions
        y10: float = 0
        u10: float = 0
        self.y1 = y10
        self.u1 = u10

        self.rms = 1

        # initialize plant model
        self.H1 = self.plant(1, 1)
        self.H_list = [self.H1]
        self.time_max = 0

        self.y1_list = []
        self.dt = 1
        self.I = 0

        self.obs = {
            "y1": float(self.y1),
            "y1ref": float(self.y1ref),
            "u1": float(self.u1),
            "rms": float(self.rms)
        }

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        terminated = False
        reward = 0

        error_var = self.noise_percentage #system noise %
        self.Δu1 = action[0]
        Δu1 = self.Δu1
        self.u1 += self.Δu1


        #calling the python model
        st = 1 #controler action time
        if self.cnt == 0:
            st = 2
        #simulation time
        self.time_max += st
        tm = np.linspace(0, self.time_max, self.time_max)

        self.time_max / st

        if self.cnt == 0:
            self.in1 = [Δu1 for i in range(st)]
        else:
            self.in1 += [Δu1 for i in range(st)]

        in_ = np.array([self.in1])

        T_delay = self.time_delay
        n_pade = 4
        (num_pade , den_pade) = control.pade(T_delay , n_pade) ##
        y1_pade = control.tf(num_pade , den_pade)

        y1_with_delay = control.series(self.H1 , y1_pade)
        io_1 = control.tf2io(y1_with_delay, input='u1', output='y1')

        (tm2 , y1_step) = control.step_response(io_1 , np.linspace(0,30 ,30))
        self.y1_step = y1_step

        t, y1_ = control.input_output_response(io_1, tm, in_, squeeze = False)
        self.y1_list = y1_
        self.y1 = y1_[0][self.cnt]

        #error
        if self.y1ref > 0:
            error = [(x - self.y1ref)**2 for x in y1_]
            self.rms = math.sqrt(np.average(error))

        # Increase time
        self.cnt += 1

        # update obs with new state values
        self.obs = {
            "y1": float(self.y1),
            "y1ref": float(self.y1ref),
            "u1": float(self.u1),
            "rms": float(self.rms)
        }
        # add noise
        for key in list(self.obs.keys()):
            val = float(self.obs[key])
            sensor_noise = self.noise_percentage   # TODO: add noise as parameter
            self.obs[key] = val + random.uniform(- val * sensor_noise , val * sensor_noise )

        # end the simulation
        if not (self.obs_space_constraints['y1']['low'] <= self.y1 <= self.obs_space_constraints['y1']['high']):
            self.obs['y1'] = np.clip(self.y1, self.obs_space_constraints['y1']['low'], self.obs_space_constraints['y1']['high'])
            terminated = True

        self.obs = np.array(list(self.obs.values()))

        info = {}
        return self.obs, reward, terminated, False, info

    def render_frame(self, mode='auto'):
        pass
