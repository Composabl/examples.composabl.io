import gymnasium as gym
import numpy as np
from composabl.agent.scenario import Scenario

class SimEnv(gym.Env):
    def __init__(self):
        #  Define Observation Space
        self.obs_space_constraints = {
            'state1': {'low': -1e12, 'high': 1e12},
            'time_counter': {'low': 0, 'high': 1e12}
        }

        low_list = [x['low'] for x in self.obs_space_constraints.values()]
        high_list = [x['high'] for x in self.obs_space_constraints.values()]

        self.observation_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        #  Define Action Space
        self.action_constraints = {
            'action1': {'low': -1e3, 'high': 1e3}
        }

        low_act_list = [x['low'] for x in self.action_constraints.values()]
        high_act_list = [x['high'] for x in self.action_constraints.values()]

        self.action_space = gym.spaces.Box(low=np.array(low_act_list), high=np.array(high_act_list))

        self.scenario: Scenario = None
        print(type(self.observation_space))

    def reset(self):
        #initial values
        self.cnt = 0
        self.value = 0

        """
        ****** Define scenario in the simulation ******
        """
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            self.obs = {
                'state1': sample["state1"],
                'time_counter': self.cnt,
                }
        else:
            self.obs = {
                'state1': self.value,
                'time_counter': self.cnt
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
        self.value += action[0]
        
        #  Update obs with new state values (dummy function)
        self.obs = {
            'state1': self.value,
            'time_counter': self.cnt
        }

        #  Reward variable definition
        reward = 0

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, reward, done, False, info

    def render(self, mode='auto'):
        pass
