import math
import numpy as np 

from composabl_core.agent import Teacher
from non_linear_mpc_model import non_lin_mpc

import matplotlib.pyplot as plt

class CSTRTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.error_history = []
        self.last_reward = 0
        self.plot = True

        if self.plot:
            plt.close("all")
            plt.figure(figsize=(10,7))
            plt.ion()
        

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        if type(transformed_obs) == dict:
            if 'observation' in list(transformed_obs.keys()):
                transformed_obs = transformed_obs['observation'][0]
                #Import MPC (self.T, self.Tc, self.Ca, self.Cref, self.Tref)
                MPC_Tc = non_lin_mpc(0, transformed_obs[3], transformed_obs[2], 
                                                        transformed_obs[0], transformed_obs[1] + action[0])
                dTc_MPC = MPC_Tc[0][0] - transformed_obs[1]
            else:
                #Import MPC
                MPC_Tc = non_lin_mpc(0, transformed_obs['Cref'], transformed_obs['Ca'], 
                                                        transformed_obs['T'], transformed_obs['Tc'] + action)
                dTc_MPC = MPC_Tc[0][0] - transformed_obs['Tc']

            #limit MPC actions between -10 and 10 degrees Celsius
            dTc_MPC = np.clip(dTc_MPC,-10,10)
            action = dTc_MPC
        return action

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        reward = math.e ** (-abs(transformed_obs['Cref'] - transformed_obs['Ca']))

        error_pct = abs(transformed_obs['Cref'] - transformed_obs['Ca']) / transformed_obs['Cref']
        self.error_history.append(error_pct)
        self.last_reward = reward
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history is None:
            return False
        else:
            if self.plot:
                self.plot_obs()

            return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False
    
    def plot_obs(self):
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot([ x["Tc"] for x in self.obs_history],'k.-',lw=2)
        plt.ylabel('Cooling Tc (K)')
        plt.legend(['Jacket Temperature'],loc='best')
        

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

    