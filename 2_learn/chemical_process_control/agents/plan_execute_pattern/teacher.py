import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from composabl import SkillTeacher
from mpc_model import mpc

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

class CSTRTeacher(SkillTeacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.error_history = []
        self.last_reward = 0
        self.count = 0
        self.metrics = 'none' #standard, fast, none

        # create metrics db
        try:
            self.df = pd.read_pickle(f"{PATH_HISTORY}/history.pkl")
            if self.metrics == 'fast':
                self.plot_metrics()
        except:
            self.df = pd.DataFrame()


    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        reward = math.e ** (-abs(float(transformed_obs['Cref']) - float(transformed_obs['Ca'])))

        error = (float(transformed_obs['Cref']) - float(transformed_obs['Ca']))**2
        self.error_history.append(error)
        rms = math.sqrt(np.mean(self.error_history))
        self.last_reward = reward
        self.count += 1

        # history metrics
        df_temp = pd.DataFrame(columns=['time','Ca','Cref','reward','rms'],data=[[self.count,transformed_obs['Ca'], transformed_obs['Cref'], reward, rms]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle(f"{PATH_HISTORY}/history.pkl")
        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history is None:
            return False
        else:
            if self.metrics == 'standard':
                try:
                    self.plot_obs()
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

            return False

    async def compute_termination(self, transformed_obs, action):
        return False

    def plot_metrics(self):
        plt.figure(1,figsize=(7,5))
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(self.reward_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['reward'],s=0.5, alpha=0.2)
        plt.ylabel('Reward')
        plt.legend(['reward'],loc='best')
        plt.title('Metrics')

        plt.subplot(3,1,2)
        plt.plot(self.rms_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['rms'],s=0.5, alpha=0.2)
        plt.ylabel('RMS error')
        plt.legend(['RMS'],loc='best')

        plt.subplot(3,1,3)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['Ca'],s=0.6, alpha=0.2)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['Cref'],s=0.6, alpha=0.2)
        plt.ylabel('Ca')
        plt.legend(['Ca'],loc='best')
        plt.xlabel('iteration')

        plt.draw()
        plt.pause(0.001)

    def plot_obs(self):
        plt.figure(2,figsize=(7,5))
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot([ x["Tc"] for x in self.obs_history],'k.-',lw=2)
        plt.ylabel('Cooling Tc (K)')
        plt.legend(['Jacket Temperature'],loc='best')
        plt.title('CSTR Live Control')


        plt.subplot(3,1,2)
        plt.plot([ x["Ca"] for x in self.obs_history],'b.-',lw=3)
        plt.plot([ x["Cref"] for x in self.obs_history],'k--',lw=2,label=r'$C_{sp}$')
        plt.ylabel('Ca (mol/L)')
        plt.legend(['Reactor Concentration','Concentration Setpoint'],loc='best')

        plt.subplot(3,1,3)
        plt.plot([ x["Tref"] for x in self.obs_history],'k--',lw=2,label=r'$T_{sp}$')
        plt.plot([ x["T"] for x in self.obs_history],'b.-',lw=3,label=r'$T_{meas}$')
        plt.ylabel('T (K)')
        plt.xlabel('Time (min)')
        plt.legend(['Temperature Setpoint','Reactor Temperature'],loc='best')

        plt.draw()
        plt.pause(0.001)
