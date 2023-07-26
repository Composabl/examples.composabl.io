#!/usr/bin/env python3
from typing import Any, Dict, SupportsFloat, Tuple
import numpy as np
import random

import composabl_ray.utils.logger as logger_util
from composabl_ray.server.server_composabl import EnvSpec, ServerComposabl, Space
from composabl.agent.scenario import Scenario

import gymnasium as gym
from gymnasium.envs.registration import EnvSpec

logger = logger_util.get_logger(__name__)

class SimEnv(gym.Env):
    def __init__(self):
        #  Define Observation Space
        self.obs_space_constraints = {
            'state1': {'low': 1, 'high': 10},
            'state2': {'low': -5, 'high': 0},
            'state3': {'low': 20, 'high': 100}
        }

        low_list = [x['low'] for x in self.obs_space_constraints.values()]
        high_list = [x['high'] for x in self.obs_space_constraints.values()]

        self.observation_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        #  Define Action Space
        self.action_constraints = {
            'action1': {'low': -0.1, 'high': 0.1},
            'action2': {'low': -0.5, 'high': 0.5},
        }

        low_act_list = [x['low'] for x in self.action_constraints.values()]
        high_act_list = [x['high'] for x in self.action_constraints.values()]

        self.action_space = gym.spaces.Box(low=np.array(low_act_list), high=np.array(high_act_list))

        self.scenario: Scenario = None

    def reset(self):
        self.cnt = 0
        """
        ****** Define scenario in the simulation ******
        """
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            self.obs = {
                'state1': sample["state1"],
                'state2': sample["state2"],
                'state3': sample["state3"]
                }
        else:
            self.obs = {
                'state1': random.uniform(self.obs_space_constraints['state1']['low'], self.obs_space_constraints['state1']['high']),
                'state2': random.uniform(self.obs_space_constraints['state2']['low'], self.obs_space_constraints['state2']['high']),
                'state3': random.uniform(self.obs_space_constraints['state3']['low'], self.obs_space_constraints['state3']['high'])
                }


        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        done = False
        #  Increase time counting
        self.cnt += 1
        
        #  Run Simulation
        #  Update obs with new state values (dummy function)
        self.obs = {}
        for key in list(self.obs.keys()):
            self.obs[key] = np.clip(self.obs[key] + action[0] + action[1],
                                    self.obs_space_constraints[key]['low'],
                                    self.obs_space_constraints[key]['high'] )

        #  Reward variable definition
        reward = 0

        #  Define rules to end the simulation
        if self.cnt == 80:
            done = True

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, reward, done, False, info

    def render(self, mode='auto'):
        pass



class ServerImpl(ServerComposabl):
    def __init__(self):
        self.env = SimEnv()

    def Make(self, env_id: str) -> EnvSpec:
        spec = {'id': 'simulation_example', 'max_episode_steps': 80}
        return spec

    def ObservationSpaceInfo(self) -> gym.Space:
        return self.env.observation_space

    def ActionSpaceInfo(self) -> gym.Space:
        return self.env.action_space

    def ActionSpaceSample(self) -> Any:
        return self.env.action_space.sample()

    def Reset(self) -> Tuple[Any, Dict[str, Any]]:
        obs, info = self.env.reset()
        return obs, info

    def Step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        return self.env.step(action)

    def Close(self):
        self.env.close()

    def SetScenario(self, scenario):
        scenario = Scenario.from_proto(scenario)
        self.env.scenario = scenario

    def GetScenario(self):
        if self.env.scenario is None:
            return Scenario({"dummy": 0})

        return self.env.scenario

    def SetRewardFunc(self, reward_func):
        self.env.set_reward_func(reward_func)

