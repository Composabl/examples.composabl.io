import math
import random
from typing import Any, Dict, Optional, SupportsFloat, Tuple

import gymnasium as gym
import numpy as np
from composabl_core.agent.scenario import Scenario


class AerialAutonomyEnv(gym.Env):
    def __init__(self):
        self.obs_space_constraints = {
            "x": {'low': -400, 'high': 400},
            "x_speed": {'low': -100, 'high': 100},
            "y": {'low': 0, 'high': 1000},
            "y_speed": {'low': -1000, 'high': 1000},
            "angle": {'low': -3.15 * 2, 'high': 3.15 * 2},
            "angle_speed": {'low': -3, 'high': 3},
        }

        self.action_constraints = {
            "delta_angle": {'low': -1, 'high': 1},
            "delta_thrust": {'low': -1, 'high': 1}
        }

        low_list = [x['low'] for x in self.obs_space_constraints.values()]
        high_list = [x['high'] for x in self.obs_space_constraints.values()]

        self.sensor_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        low_act_list = [x['low'] for x in self.action_constraints.values()]
        high_act_list = [x['high'] for x in self.action_constraints.values()]

        self.action_space = gym.spaces.Box(low=np.array(low_act_list), high=np.array(high_act_list))

        self.state_models = {}
        self.reward_models = {}
        self.scenario: Scenario = None

        self.x_obs0 = 0
        self.x_speed0 = 0
        self.y_obs0 = 1000
        self.y_speed0 = -80
        self.angle0 = -np.pi / 2
        self.ang_speed0 = 0

    def starship_simulation(self, x, u):
        g = 9.8
        m = 100000 # kg
        min_thrust = 880 * 1000 # N
        max_thrust = 1 * 2210 * 1000 # kN

        length = 50 # m
        width = 10

        # Inertia for a uniform density rod
        I = (1 / 12) * m * length**2

        deg_to_rad = 0.01745329

        max_gimble = 20  * deg_to_rad
        min_gimble = -max_gimble

        theta = x[4]

        thrust = u[0]
        thrust_angle = u[1]

        # Horizontal force
        F_x = max_thrust * thrust * math.sin(thrust_angle + theta)
        x_dot = x[1]
        x_dotdot = (F_x) / m

        # Vertical force
        F_y = max_thrust * thrust * math.cos(thrust_angle + theta)
        y_dot = x[3]
        y_dotdot = (F_y) / m - g

        # Torque
        T = -length / 2 * max_thrust * thrust * math.sin(thrust_angle)
        theta_dot = x[5]
        theta_dotdot = T / I

        return [x_dot, x_dotdot, y_dot, y_dotdot, theta_dot, theta_dotdot]

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            options: Optional[dict] = None,
            x_obs0: float = 0,
            x_speed0: float = 0,
            y_obs0: float = 1000,
            y_speed0: float = -80,
            angle0: float = -np.pi / 2,
            ang_speed0: float = 0
    ):
        '''
        # x[0] = x position (m)
        # x[1] = x velocity (m/)
        # x[2] = y position (m)
        # x[3] = y velocity (m/s)
        # x[4] = angle (rad)
        # x[5] = angular velocity (rad/s)

        # u[0] = thrust (percent)
        # u[1] = thrust angle (rad)

        '''
        super().reset(seed=seed)
        self.cnt = 0
        self.min_thrust = 880 * 1000 # N
        self.max_thrust = 1 * 2210 * 1000 # kN

        deg_to_rad = 0.01745329

        self.max_gimble = 20  * deg_to_rad
        self.min_gimble = -self.max_gimble

        # Define scenario in the simulation ******
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])
        else:
            self.x_obs0 = x_obs0
            self.x_speed0 = x_speed0
            self.y_obs0 = y_obs0
            self.y_speed0 = y_speed0
            self.angle0 = angle0
            self.ang_speed0 = ang_speed0

        # Set the number of steps and the timestep (dt)
        steps = 400
        self.t_step = 0.04
        self.cnt = 0

        self.x = np.zeros((steps + 1, 6))
        self.u = np.zeros((steps + 1, 2))

        self.x[0, :] = [self.x_obs0, self.x_speed0, self.y_obs0, self.y_speed0, self.angle0, self.ang_speed0]
        self.x[steps - 1, :] = [0, 0, 0, 0, 0, 0]

        self.x_obs = self.x[self.cnt, 0]
        self.x_speed = self.x[self.cnt, 1]
        self.y_obs = self.x[self.cnt, 2]
        self.y_speed = self.x[self.cnt, 3]
        self.angle = self.x[self.cnt, 4]
        self.ang_speed = self.x[self.cnt, 5]

        self.t = 0
        self.a = 0
        self.reward_value = 0

        self.obs = {
            "x": self.x_obs,
            "x_speed": self.x_speed,
            "y": self.y_obs,
            "y_speed": self.y_speed,
            "angle": self.angle,
            "angle_speed": self.ang_speed
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

        def sumsqr(lt):
            v = sum([x**2 for x in lt])
            return v

        thrust = action[0]
        angle = action[1]

        actuator_noise = 0
        self.t += thrust + random.uniform(-actuator_noise * thrust, actuator_noise * thrust)
        self.a += angle + random.uniform(-actuator_noise * angle, actuator_noise * angle)

        self.t = np.clip(self.t, 0.4, 1)
        self.a = np.clip(self.a, self.min_gimble, self.max_gimble)

        # update u
        self.u[self.cnt, 0] = self.t
        self.u[self.cnt, 1] = self.a

        res = self.starship_simulation(self.x[self.cnt, :], self.u[self.cnt, :])
        res = [v * self.t_step for v in res]

        self.x[self.cnt + 1, :] = [sum(value) for value in zip(self.x[self.cnt, :], res)]

        # Increase time
        self.cnt += 1
        #update values
        self.x_obs = self.x[self.cnt, 0]
        self.x_speed = self.x[self.cnt, 1]
        self.y_obs = self.x[self.cnt, 2]
        self.y_speed = self.x[self.cnt, 3]
        self.angle = self.x[self.cnt, 4]
        self.ang_speed = self.x[self.cnt, 5]

        #self.x_goal = obs['desired_goal'][0]
        #self.y_goal = obs['desired_goal'][1]

        # update obs with new state values
        self.obs = {
            "x": self.x_obs,
            "x_speed": self.x_speed,
            "y": self.y_obs,
            "y_speed": self.y_speed,
            "angle": self.angle,
            "angle_speed": self.ang_speed,
        }
        # add noise
        for key in list(self.obs.keys()):
            val = float(self.obs[key])
            sensor_noise = 0.0   # TODO: add noise as parameter
            self.obs[key] = val + random.uniform(- val * sensor_noise , val * sensor_noise)

        # end the simulation
        if self.y_obs < 0:
            terminated = True
        elif not self.obs_space_constraints['x']['low'] <= self.x_obs <= self.obs_space_constraints['x']['high']:
            terminated = True

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, reward, terminated, False, info

    def render(self, mode='auto'):
        pass
