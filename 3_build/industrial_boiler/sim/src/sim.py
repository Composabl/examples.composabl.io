# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import math
import random
from typing import Optional

import control
import gymnasium as gym
import numpy as np
from composabl_core.agent.scenario import Scenario


class Env(gym.Env):
    def __init__(self):
        self.obs_space_constraints = {
            "y1": {"low": 0, "high": 5},  # drum level
            "y2": {"low": 0, "high": 20},  # drum pressure
            "y3": {"low": 0, "high": 600},  # drum temperature
            "y1ref": {"low": 0, "high": 400},
            "y2ref": {"low": 0, "high": 400},
            "y3ref": {"low": 0, "high": 400},
            "u1": {"low": 0, "high": 120},  # feed water flow rate
            "u2": {"low": 0, "high": 7},  # fuel flow rate
            "u3": {"low": 0, "high": 10},  # spray flow rate
            "rms": {"low": 0, "high": 100},
            "eff_nox_red": {"low": 0, "high": 400},
            "nox_emissions": {"low": 0, "high": 400},
            "total_nox_emissions": {"low": 0, "high": 400},
        }

        self.action_constraints = {
            "du1": {"low": -20, "high": 20},
            "du2": {"low": -0.017, "high": 0.017},
            "du3": {"low": -2, "high": 2},
        }

        low_list = [x["low"] for x in self.obs_space_constraints.values()]
        high_list = [x["high"] for x in self.obs_space_constraints.values()]

        self.sensor_space = gym.spaces.Box(
            low=np.array(low_list), high=np.array(high_list)
        )

        low_act_list = [x["low"] for x in self.action_constraints.values()]
        high_act_list = [x["high"] for x in self.action_constraints.values()]

        self.action_space = gym.spaces.Box(
            low=np.array(low_act_list), high=np.array(high_act_list)
        )

        self.state_models = {}
        self.reward_models = {}
        self.scenario: Scenario = None

        # initial conditions
        self.y1 = 1  # Drum Level
        self.y2 = 6.45  # Drum pressure
        self.y3 = 466.7  # Drum Temperature

        self.u1 = 40.68  # Feed Water Flow rate
        self.u2 = 2.102  # Fuel Flow rate
        self.u3 = 0  # Spray Flow rate
        self.eff_nox_red = 0.7
        self.signal = "y1"
        self.noise_percentage = 0

        # Scenario Init
        self.scenario = None

    def plant(self, i, j):
        # Build the plant model from transfer functions
        # time step (seconds) between state updates
        Δt = 1
        num = [
            [[-0.16e-3, 0.052e-3, 0.0014e-3], [3.1e-3, -0.032e-3], [0]],
            [[-0.0395e-3], [2.51e-3], [0.588e-3, 0.2015e-3, 0.0009e-3]],
            [[-0.00118, 0.000139], [0.448, 0.0011], [0.582, -0.0243]],
        ]
        den = [
            [[1, 0.0168, 0], [1, 0.0215, 0], [1]],
            [[1, 0.018], [1, 0.0157], [1, 0.0352, 0.000142]],
            [[1, 0.01852], [1, 0.0127, 0.000095], [1, 0.1076, 0.00104]],
        ]

        dt = 0
        sys1 = control.tf(num[i - 1][j - 1], den[i - 1][j - 1], dt=dt)

        return sys1

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        """ """
        self.cnt = 0

        # Define scenario in the simulation

        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                if key in ["signal", "eff_nox_red", "noise_percentage"]:
                    setattr(self, key, sample[key])

        self.rms = 1

        # TODO: include option that user can choose variable and send SP
        if self.signal == "y1":  # Drum level increase 10%
            self.y1ref = 1.1 * self.y1
            self.y2ref = 0
            self.y3ref = 0
        elif self.signal == "y2":  # Drum pressure increase 5%
            self.y1ref = 0
            self.y2ref = 1.05 * self.y2
            self.y3ref = 0
        elif self.signal == "y3":  # Temperature increase 20%
            self.y1ref = 0
            self.y2ref = 0
            self.y3ref = 1.2 * self.y3

        # initialize plant model
        self.H1 = self.plant(1, 1)
        self.H2 = self.plant(1, 2)
        self.H3 = self.plant(1, 3)

        self.H4 = self.plant(2, 1)
        self.H5 = self.plant(2, 2)
        self.H6 = self.plant(2, 3)

        self.H7 = self.plant(3, 1)
        self.H8 = self.plant(3, 2)
        self.H9 = self.plant(3, 3)

        self.H_list = [
            self.H1,
            self.H2,
            self.H3,
            self.H4,
            self.H5,
            self.H6,
            self.H7,
            self.H8,
            self.H9,
        ]

        self.time_max = 0

        self.nox_emissions = 0
        self.total_nox_emissions = 0
        self.nox_emissions_yr = 0
        self.total_fuel_used = 0  # kg/episode
        self.fuel_used_yr = 0

        self.obs = {
            "y1": float(self.y1),
            "y2": float(self.y2),
            "y3": float(self.y3),
            "y1ref": float(self.y1ref),
            "y2ref": float(self.y2ref),
            "y3ref": float(self.y3ref),
            "u1": float(self.u1),
            "u2": float(self.u2),
            "u3": float(self.u3),
            "rms": float(self.rms),
            "eff_nox_red": float(self.eff_nox_red),
            "nox_emissions": float(self.nox_emissions),
            "total_nox_emissions": float(self.total_nox_emissions),
        }

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        terminated = False
        discount = 0
        reward = 0

        error_var = self.noise_percentage  # system noise %
        Δu1 = action[0]
        Δu2 = action[1]
        Δu3 = action[2]

        # Python Dynamic model
        st = 2  # controler action time (1 step = 20s)
        # simulation time
        self.time_max += st
        tm = np.linspace(0, self.time_max, self.time_max)  # 20 sec

        u1_list = []  # 0 <= u1 <= 120
        u2_list = []  # 0 <= u2 <= 7  #-0.017 <= du2 <= 0.017
        u3_list = []  # 0 <= u3 <= 10

        self.time_max / st

        if self.cnt == 0:
            self.in1 = [Δu1 for i in range(st)]
            self.in2 = [Δu2 for i in range(st)]
            self.in3 = [Δu3 for i in range(st)]
        else:
            self.in1 += [Δu1 for i in range(st)]
            self.in2 += [Δu2 for i in range(st)]
            self.in3 += [Δu3 for i in range(st)]

        in_ = [self.in1, self.in2, self.in3]

        # Drum Level
        y1 = control.parallel(self.H1, self.H2, self.H3)
        io_1 = control.tf2io(self.H1, input="u1", output="y1")
        io_2 = control.tf2io(self.H2, input="u2", output="y2")
        io_3 = control.tf2io(self.H3, input="u3", output="y3")
        sumblk = control.summing_junction(inputs=["y1", "y2", "y3"], output="y")
        io_y1 = control.interconnect(
            (io_1, io_2, io_3, sumblk), inputs=["u1", "u2", "u3"], output="y"
        )

        t, y1_ = control.input_output_response(io_y1, tm, in_)
        self.y1 += y1_[0][-1]

        # Drum Pressure
        y1 = control.parallel(self.H4, self.H5, self.H6)
        io_1 = control.tf2io(self.H4, input="u1", output="y1")
        io_2 = control.tf2io(self.H5, input="u2", output="y2")
        io_3 = control.tf2io(self.H6, input="u3", output="y3")
        sumblk = control.summing_junction(inputs=["y1", "y2", "y3"], output="y")
        io_y1 = control.interconnect(
            (io_1, io_2, io_3, sumblk), inputs=["u1", "u2", "u3"], output="y"
        )

        t, y2_ = control.input_output_response(io_y1, tm, in_)
        self.y2 += y2_[0][-1]

        # Temperature
        y1 = control.parallel(self.H7, self.H8, self.H9)
        io_1 = control.tf2io(self.H7, input="u1", output="y1")
        io_2 = control.tf2io(self.H8, input="u2", output="y2")
        io_3 = control.tf2io(self.H9, input="u3", output="y3")
        sumblk = control.summing_junction(inputs=["y1", "y2", "y3"], output="y")
        io_y1 = control.interconnect(
            (io_1, io_2, io_3, sumblk), inputs=["u1", "u2", "u3"], output="y"
        )

        t, y3_ = control.input_output_response(io_y1, tm, in_)
        self.y3 += y3_[0][-1]

        # Clip unvalid values
        self.y1 = np.clip(self.y1, a_min=0, a_max=None)
        self.y2 = np.clip(self.y2, a_min=0, a_max=None)
        self.y3 = np.clip(self.y3, a_min=0, a_max=None)

        self.u1 = np.clip(self.u1, a_min=0, a_max=120)
        self.u2 = np.clip(self.u2, a_min=0, a_max=7)
        self.u3 = np.clip(self.u3, a_min=0, a_max=10)

        # Increase time
        self.cnt += 1

        # Emissions
        self.total_fuel_used += self.u2 * 60
        self.fuel_used_yr = (
            (60 * self.total_fuel_used / self.cnt) * 8 * 22 * 12 / 1000
        )  # ton/yr estimation
        EF = 2.24 * (10e-3)
        CE = self.eff_nox_red  # 0.7 #low efficiency from SCR
        self.nox_emissions_yr = self.fuel_used_yr * EF * (1 - CE)  # kg/yr
        self.nox_emissions = self.nox_emissions_yr / (12 * 22 * 8)  # kg/hr

        self.total_nox_emissions += self.nox_emissions

        # error
        if self.y1ref > 0:
            error = [(x - self.y1ref) ** 2 for x in y1_]
            self.rms = math.sqrt(np.average(error))
        elif self.y2ref > 0:
            error = [(x - self.y2ref) ** 2 for x in y2_]
            self.rms = math.sqrt(np.average(error))
        elif self.y3ref > 0:
            error = [(x - self.y3ref) ** 2 for x in y3_]
            self.rms = math.sqrt(np.average(error))

        # update obs with new state values
        self.obs = {
            "y1": float(self.y1),
            "y2": float(self.y2),
            "y3": float(self.y3),
            "y1ref": float(self.y1ref),
            "y2ref": float(self.y2ref),
            "y3ref": float(self.y3ref),
            "u1": float(self.u1),
            "u2": float(self.u2),
            "u3": float(self.u3),
            "rms": float(self.rms),
            "eff_nox_red": float(self.eff_nox_red),
            "nox_emissions": float(self.nox_emissions),
            "total_nox_emissions": float(self.total_nox_emissions),
        }
        # add noise
        for key in list(self.obs.keys()):
            val = float(self.obs[key])
            sensor_noise = self.noise_percentage  # TODO: add noise as parameter
            self.obs[key] = val + random.uniform(
                -val * sensor_noise, val * sensor_noise
            )

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, reward, terminated, False, info

    def render(self, mode="auto"):
        pass
