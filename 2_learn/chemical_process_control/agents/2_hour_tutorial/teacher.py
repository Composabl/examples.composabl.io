import os
from composabl import Teacher
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"

#Skills are the building blocks of intelligent autonomous agents.
#Teaching allows you to define these AI building blocks so that your agent can succeed at complex tasks in dynamic conditions
#This is an example of a base class to show the full structure of a teacher and all the associated elements.
class BaseCSTR(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.rms_history = []
        self.last_reward = 0
        self.count = 0
        self.title = 'CSTR Live Control'
        self.history_path = f"{PATH_HISTORY}/history.pkl"
        self.metrics = 'none' #standard, fast, none

        # Create history folder if it doesn't exist
        if not os.path.exists(PATH_HISTORY):
            os.mkdir(PATH_HISTORY)

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

    def transform_sensors(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_sensor_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)


        error = (float(transformed_obs['Ca']) - float(transformed_obs['Cref']))**2
        self.error_history.append(error)
        rms = math.sqrt(np.mean(self.error_history))
        self.rms_history.append(rms)

        # minimize error
        if error == 0:
            reward = float(1/(math.sqrt(error + 0.00000000001)))
        else:
            reward = float(1/(math.sqrt(error)))
        self.reward_history.append(reward)

        self.count += 1

        # history metrics
        if self.metrics != 'none':
            df_temp = pd.DataFrame(columns=['time','Ca','Cref','reward','rms'],data=[[self.count,transformed_obs['Ca'], transformed_obs['Cref'], reward, rms]])
            self.df = pd.concat([self.df, df_temp])
            self.df.to_pickle(self.history_path)

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        success = False
        if self.obs_history is None:
            success = False
        else:
            if self.metrics == 'standard':
                try:
                    self.plot_obs()
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

        return success

    def compute_termination(self, transformed_obs, action):
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
        plt.title(self.title)


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

#This is the teacher for the Start Reaction skill. This will need
#Copy this entire class 2 times and re-name them to reflect the second and third skills in the agent design.
#Ensure that the self.title and self.history_path variables are also changed to reflect the names of the skills.
class StartReactionTeacher(BaseCSTR):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title = 'CSTR Live Control - StartReaction skill'
        self.history_path = f"{PATH_HISTORY}/StartReaction_history.pkl"

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)


        error = (float(transformed_obs['Ca']) - float(transformed_obs['Cref']))**2
        self.error_history.append(error)
        rms = math.sqrt(np.mean(self.error_history))
        self.rms_history.append(rms)

        # minimize error
        reward = 1 / rms
        self.reward_history.append(reward)

        self.count += 1

        # history metrics
        if self.metrics != 'none':
            df_temp = pd.DataFrame(columns=['time','Ca','Cref','reward','rms'],data=[[self.count,transformed_obs['Ca'], transformed_obs['Cref'], reward, rms]])
            self.df = pd.concat([self.df, df_temp])
            self.df.to_pickle(self.history_path)

        return reward

    def compute_termination(self, transformed_obs, action):
        return False


#This is the teacher for the Selector Skill.
class CSTRTeacher(BaseCSTR):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.error_history = []
        self.rms_history = []
        self.last_reward = 0
        self.count = 0
        self.title = 'CSTR Live Control - Selector skill'
        self.history_path = f"{PATH_HISTORY}/selector_history.pkl"
        self.plot = False
        self.metrics = 'none' #standard, fast, none

        if self.plot:
            plt.close("all")
            plt.figure(figsize=(7,5))
            plt.title(self.title)
            plt.ion()

        # create metrics db
        try:
            self.df = pd.read_pickle(self.history_path)

            if self.metrics == 'fast':
                self.plot_metrics()
        except Exception:
            self.df = pd.DataFrame()

