import os
import pandas as pd
from composabl import Teacher
import numpy as np
import matplotlib.pyplot as plt

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"

class BalanceTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.cnt = 0
        self.plot = False
        self.metrics = 'none'

        # create metrics db
        try:
            self.df = pd.read_pickle(f"{PATH_HISTORY}/db.pkl")

            #if self.metrics == 'fast':
            #    self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["inventory",
                "balance",
                "num_ordered",
                "holding_cost",
                "cost_price",
                "delay_days_until_delivery",
                "customer_demand_min",
                "customer_demand_max",
                "selling_price"]

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        self.cnt += 1

        reward = float(transformed_obs["balance"])/1e7

        if self.metrics != 'none':
            # history metrics
            df_temp = pd.DataFrame(columns=['inventory','balance','num_ordered','order_cutoff','reward','time'],
            data=[[transformed_obs['inventory'],transformed_obs['balance'],transformed_obs['num_ordered'],action[0],reward,self.cnt]])
            self.df = pd.concat([self.df, df_temp])
            self.df.to_pickle(f"{PATH_HISTORY}/db.pkl")
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history != None:
            if self.plot:
                self.plot_obs()

        return False

    def compute_termination(self, transformed_obs, action):
        return False

    def plot_obs(self):
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot([x['inventory'] for x in self.obs_history])
        plt.xlabel("Simulation time (days)")
        plt.ylabel("Inventory level")

        plt.subplot(3,1,2)
        plt.plot([x['balance'] for x in self.obs_history])
        plt.xlabel("Simulation time (days)")
        plt.ylabel("Balance History ($)")

        plt.subplot(3,1,3)
        plt.plot([x['num_ordered'] for x in self.obs_history] )
        plt.xlabel("Simulation time (days)")
        plt.ylabel("Order History")

        plt.draw()
        plt.pause(0.001)
