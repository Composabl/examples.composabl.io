import numpy as np
from composabl import Teacher
import matplotlib.pyplot as plt
import pandas as pd

class LevelTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['y1', 'y2', 'y3', 'y1ref', 'y2ref', 'y3ref', 'u1', 'u2', 'u3']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        error = abs(np.mean(np.array(self.obs_history)[:, 0]) - np.mean(np.array(self.obs_history)[:, 3]))

        if error != 0:
            reward = 1 / error
        else:
            reward = 1e12

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class PressureTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['y1', 'y2', 'y3', 'y1ref', 'y2ref', 'y3ref', 'u1', 'u2', 'u3']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        error = abs(np.mean(np.array(self.obs_history)[:, 1]) - np.mean(np.array(self.obs_history)[:, 4]))

        if error != 0:
            reward = 1 / error
        else:
            reward = 1e12

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False


class TemperatureTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.count = 0
        self.plot = True
        self.metrics = 'fast' #standard, fast

        if not self.plot:
            plt.close("all")
            plt.figure(figsize=(10,7))
            plt.ion()
        
        # create metrics db
        try:
            self.df = pd.read_pickle('./boiler/history.pkl')
            if self.metrics == 'fast':
                self.plot_metrics()
        except:
            self.df = pd.DataFrame()

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ['y1', 'y2', 'y3', 'y1ref', 'y2ref', 'y3ref', 'u1', 'u2', 'u3']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [list(transformed_obs.values())]
            return 0
        else:
            self.obs_history.append(list(transformed_obs.values()))

        error = abs(np.mean(np.array(self.obs_history)[:, 2]) - np.mean(np.array(self.obs_history)[:, 5]))
        #error = [(x - self.y3ref)**2 for x in y3_]
        #self.rms = math.sqrt(np.average(error))

        if error != 0:
            reward = 1 / error
        else:
            reward = 1e12

        self.reward_history.append(reward)
        self.count += 1
        # history metrics
        df_temp = pd.DataFrame(columns=['time','y1','y2','y3','y1ref', 'y2ref', 'y3ref','u1','u2','reward'],
                               data=[[self.count,transformed_obs['y1'], transformed_obs['y2'],transformed_obs['y3'], transformed_obs['y1ref'],
                                      transformed_obs['y2ref'], transformed_obs['y3ref'],transformed_obs['u1'], transformed_obs['u2'], reward]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle("./boiler/history.pkl")  

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history == None:
            return False
        else:
            success = len(self.obs_history) >= 400

            if self.plot and len(self.df) != 0:
                self.plot_obs()

            if self.metrics == 'standard':
                try:
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

            return success

    def compute_termination(self, transformed_obs, action):
        #if abs(transformed_obs['y2']) >= 2:
        #    return True
        if self.count > 10:
            if abs(transformed_obs['y1']) <= 0.1:
                return True
            if abs(transformed_obs['y3']) < 300 or abs(transformed_obs['y3']) > 600:
                return True
            if abs(transformed_obs['y1']) > 4:
                return True
        return False
    
    def plot_obs(self):
        plt.clf()
        plt.subplot(6,1,1)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y1']))],self.df.reset_index()['y1'],'b.-',lw=2)
        
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y1']))],[self.df.reset_index()['y1ref'] for x in range(len(self.df.reset_index()['y1']))],'r--',lw=1)   
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y1']))],[1-0.05 for x in range(len(self.df.reset_index()['y1']))],'g--',lw=1)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y1']))],[1+0.05 for x in range(len(self.df.reset_index()['y1']))],'g--',lw=1)
        plt.ylabel('Y1')
        plt.legend(['y1'],loc='best')
        
        plt.subplot(6,1,2)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y2']))],self.df.reset_index()['y2'],'b.-',lw=2)
        
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y2']))],[self.df.reset_index()['y2ref'] for x in range(len(self.df.reset_index()['y2']))],'r--',lw=1)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y2']))],[self.df.reset_index()['y2ref']-0.01 for x in range(len(self.df.reset_index()['y2']))],'g--',lw=1)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y2']))],[self.df.reset_index()['y2ref']+0.01 for x in range(len(self.df.reset_index()['y2']))],'g--',lw=1)
        plt.ylabel('Y2')
        plt.legend(['y2'],loc='best') 
        

        plt.subplot(6,1,3)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['u1']))],self.df.reset_index()['u1'],'k--',lw=2,label=r'$C_{sp}$')
        plt.ylabel('U1')
        plt.legend(['U1 - Feedwater Flowrate'],loc='best')

        plt.subplot(6,1,4)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['u2']))],self.df.reset_index()['u2'],'k--',lw=2,label=r'$T_{sp}$')
        plt.ylabel('u2')
        plt.xlabel('Time (min)')
        plt.legend(['U2 - Flue Flowrate'],loc='best')

        plt.subplot(6,1,5)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y3']))],self.df.reset_index()['y3'],'r--',lw=2,label=r'$T_{sp}$')
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y3']))],[466-10 for x in range(len(self.df.reset_index()['y3']))],'g--',lw=1)
        plt.plot([i/2 for i in range(len(self.df.reset_index()['y3']))],[466+10 for x in range(len(self.df.reset_index()['y3']))],'g--',lw=1)
        plt.ylabel('y3')
        plt.xlabel('Time (min)')
        plt.legend(['Y3 - Temperature'],loc='best')

        '''plt.subplot(6,1,6)
        plt.plot([i/2 for i in range(len(nox_list))],nox_list,'k.-',lw=2,label=r'$T_{sp}$')
        plt.ylabel('NOx Emission kg/hr')
        plt.xlabel('Time (min)')
        plt.legend(['NOx Emission kg/hr'],loc='best')'''
        

        plt.draw()
        plt.pause(0.001)
