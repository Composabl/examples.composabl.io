import random
import sqlite3

import gymnasium as gym
import numpy as np
from composabl_core.agent.scenario import Scenario


class Env(gym.Env):
    def __init__(self):
        '''
        observation_variables = 6 :
        actions = 2 :
            de: elevator angle variation

        '''
        #print files
        #print(os.listdir())
        #self.df = pd.read_csv('src/fraud_detection_dataset.csv')
        #print(self.df)
        self.vars = ['step', 'amount', 'oldbalanceOrg','newbalanceOrig', 'oldbalanceDEst', 'newbalanceDest']
        self.select_vars = str(self.vars).replace('[', '').replace(']','').replace("'","")
        self.target = 'isFraud'
        self.select_target = str(self.target).replace("'", "")
        self.conn = sqlite3.connect('src/fraud_detection_db.db')

        obs_space = {}
        for var in self.vars:
            obs_space[var] = {"low": -1e20, "high": 1e20}

        low_list = [x['low'] for x in obs_space.values()]
        high_list = [x['high'] for x in obs_space.values()]

        self.observation_space = gym.spaces.Box(low=np.array(low_list), high=np.array(high_list))

        self.action_space = gym.spaces.Discrete(2)

        self.count_cols = self.conn.execute("SELECT COUNT(*) from fraud_detection").fetchall()[0][0]

        self.scenario = None

    def set_scenario(self, scenario):
        self.scenario = scenario

    def reset(self):
        self.done = False
        self.cnt = 0

        # Define scenario in the simulation
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])

        self.start = random.randint(0,self.count_cols - 100) # max ite per episode

        obs = self.conn.execute(f"SELECT {self.select_vars} FROM fraud_detection LIMIT 1 OFFSET {self.start};").fetchall()

        self.obs = np.array(list(obs[0]))
        info = {}
        return self.obs, info

    def step(self, action):
        self.done = False

        # get target
        target = self.conn.execute(f"SELECT {self.select_target} FROM fraud_detection LIMIT 1 OFFSET {self.start};").fetchall()
        target = target[0][0]

        #Increase time and start
        self.cnt +=1
        self.start += 1

        print('ACTION:', action, 'TARGET:', target)
        if (action == target):
            self.reward = 1
        else:
            self.reward = -1

        self.obs = self.conn.execute(f"SELECT {self.select_vars} FROM fraud_detection LIMIT 1 OFFSET {self.start};").fetchall()[0]

        # end the simulation
        if self.cnt == self.count_cols:
            self.done = True
        elif self.cnt >= 100:
            self.done = True

        info = {}
        return self.obs, self.reward, self.done, False, info

    def render_frame(self, mode='human', close=False):
        print("render")
