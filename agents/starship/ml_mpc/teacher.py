from composabl import Teacher
import math
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, rc
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from ipywidgets import IntProgress
from IPython.display import display
import numpy as np
import pandas as pd
import pickle

class DRLMPCTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.action_history = []
        self.thrust_history = []
        self.angle_history = []
        self.t = 0.4
        self.a = -3.14/2
        self.count = 0
        self.cnt_mpc = 0
        self.plot = True
        self.metrics = 'fast' #standard, fast

        with open('./starship/data/data_mpc.pkl', 'rb') as file:
            self.mpc_values = pickle.load(file)
        file.close()

        self.a_model = pickle.load(open('./starship/data/angle_model.pkl', 'rb'))
        self.t_model = pickle.load(open('./starship/data/thrust_model.pkl','rb'))

        if not self.plot:
            plt.close("all")
            plt.figure(figsize=(10,7))
            plt.ion()

        # create metrics db
        try:
            self.df = pd.read_pickle('./starship/mpc_history.pkl')
            if self.metrics == 'fast':
                self.plot_metrics()
        except:
            self.df = pd.DataFrame()

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        if type(transformed_obs) != dict:
            X = transformed_obs
        else:
            X = pd.DataFrame(data=[[transformed_obs['x'], transformed_obs['x_speed'], transformed_obs['y'],
            transformed_obs['y_speed'], transformed_obs['angle'], transformed_obs['ang_speed']]],
            columns=['x_obs','x_speed', 'y_obs', 'y_speed', 'angle', 'ang_speed'])
     
        t = self.t_model.predict([X])[0] + action[0]
        a = self.a_model.predict([X])[0] + action[1]
    
        action = [t, a]
        #action = [self.mpc_values['angle'][self.cnt_mpc+1],self.mpc_values['angle'][self.cnt_mpc+1]]
        return action

    def filtered_observation_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    def compute_reward(self, transformed_obs, action):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        r1 = math.e**(-1*(transformed_obs["angle"] - self.mpc_values['angle'][self.cnt_mpc+1])**2)
        r2 = math.e**(-1*(transformed_obs["ang_speed"] - self.mpc_values['angle_speed'][self.cnt_mpc+1])**2)
        r3 = math.e**(-1*(transformed_obs["x"] - self.mpc_values['x'][self.cnt_mpc+1])**2)
        r4 = math.e**(-1*(transformed_obs["x_speed"] - self.mpc_values['x_speed'][self.cnt_mpc+1])**2)
        r5 = math.e**(-1*(transformed_obs["y"] - self.mpc_values['y'][self.cnt_mpc+1])**2)
        r6 = math.e**(-1*(transformed_obs["y_speed"] - self.mpc_values['y_speed'][self.cnt_mpc+1])**2)

        '''if transformed_obs["y"] <= 300:
            reward = (r1 + r3 + 2*r4 + 2*r5 + 2*r6) /8
        elif transformed_obs["y"] > 300 :
            reward = (2*r1 + 2*r3 + r5 + r6) /6'''

        reward = (r1 + r2 + r3 + r4 + r5 + r6) / 6

        #self.t += action[0]
        #self.a += action[1]
        self.t = action[0]
        self.a = action[1]

        self.t = np.clip(self.t,0.4,1)
        self.a = np.clip(self.a, -3.15, 3.15)

        self.action_history.append(action)
        self.thrust_history.append([self.t, self.a])

        self.reward_history.append(reward)
        self.angle_history.append(transformed_obs['angle'])
        self.count += 1
        self.cnt_mpc += 1
        # history metrics
        df_temp = pd.DataFrame(columns=['time','x','y','x_speed', 'y_speed', 'angle', 'angle_speed','reward'],
                               data=[[self.count,transformed_obs['x'], transformed_obs['y'],transformed_obs['x_speed'], transformed_obs['y_speed'],
                                      transformed_obs['angle'], transformed_obs['ang_speed'], reward]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle("./starship/mpc_history.pkl")

        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        if self.plot:
            if len(self.obs_history) > 100 and len(self.obs_history) % 100 == 0:
                self.plot_obs('Stabilization')

        if self.obs_history == None:
            return False
        else:
            success = len(self.obs_history) >= 400

            if self.metrics == 'standard':
                try:
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

            return success

    def compute_termination(self, transformed_obs, action):
        if abs(transformed_obs['angle']) > 5:
            return True
        else:
            return False

    def plot_metrics(self):
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(self.reward_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['reward'],s=0.5, alpha=0.2)
        plt.ylabel('Reward')
        plt.legend(['reward'],loc='best')

        plt.subplot(3,1,2)
        #plt.plot(self.rms_history, 'r.-')
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['x'],s=0.5, alpha=0.2)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['y'],s=0.5, alpha=0.2)
        plt.ylabel('X and Y')
        plt.legend(['x', 'y'],loc='best')

        plt.subplot(3,1,3)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['angle'],s=0.6, alpha=0.2)
        plt.plot(self.angle_history, 'r.-')
        plt.ylabel('angle')
        plt.legend(['angle'],loc='best')
        plt.xlabel('iteration')

        plt.subplot(3,1,3)
        plt.scatter(self.df.reset_index()['time'],self.df.reset_index()['angle'],s=0.6, alpha=0.2)
        plt.plot(self.angle_history, 'r.-')
        plt.ylabel('angle')
        plt.legend(['angle'],loc='best')
        plt.xlabel('iteration')

        #plt.show()
        plt.draw()
        plt.pause(0.001)

    def plot_obs(self, title='Starship'):
        #x = [ x["x"] for x in self.obs_history[:]]
        x = np.array([ list(x.values()) for x in self.obs_history[:]])
        u = np.array(self.thrust_history[:])
        length = 50 # m
        width = 10
        #steps = 400
        steps = len(x)

        t_step= 0.04
        final_time_step = t_step
        duration = t_step * steps

        #print("Generating Animation")
        f = IntProgress(min = 0, max = steps)
        #display(f)

        x_t = x
        u_t = u

        fig = plt.figure(figsize = (5, 5), constrained_layout=False)

        ax1 = fig.add_subplot(111)

        ln6, = ax1.plot([], [], '--', linewidth = 2, color = 'orange')

        ln2, = ax1.plot([], [], linewidth = 2, color = 'tomato')
        ln1, = ax1.plot([], [], linewidth = 5, color = 'lightblue')

        #plt.axis('off')
        plt.tight_layout()

        ax1.set_xlim(-400, 400)
        ax1.set_ylim(-50, 1000)
        ax1.set_aspect(1)

        def update(i):
            rocket_theta = x_t[i, 4]

            rocket_x = x_t[i, 0]
            rocket_x_points = [rocket_x + length/2 * math.sin(rocket_theta), rocket_x - length/2 * math.sin(rocket_theta)]

            rocket_y = x_t[i, 2]
            rocket_y_points = [rocket_y + length/2 * math.cos(rocket_theta), rocket_y - length/2 * math.cos(rocket_theta)]

            ln1.set_data(rocket_x_points, rocket_y_points)

            thrust_mag = u_t[i, 0]
            thrust_angle = -u_t[i, 1]

            flame_length = (thrust_mag) * 50

            flame_x_points = [rocket_x_points[1], rocket_x_points[1] + flame_length * math.sin(thrust_angle - rocket_theta)]
            flame_y_points = [rocket_y_points[1], rocket_y_points[1] - flame_length * math.cos(thrust_angle - rocket_theta)]

            ln2.set_data(flame_x_points, flame_y_points)

            ln6.set_data(x_t[:i, 0], x_t[:i, 2])

            f.value += 1

        anim = FuncAnimation(fig, update, np.arange(0, steps-1, 1), interval= final_time_step * 1000)

        plt.title(title)
        plt.show(block=False)
        plt.pause(duration)
        plt.close("all")