import re
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
from mpc_actions import thrust_optm, angle_optm

class DRLMPCTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.action_history = []
        self.thrust_history = []
        self.angle_history = []
        self.error_history = []
        self.t = 0.4
        self.a = -3.14/2

        self.t = 0.0
        self.a = 0.0

        self.count = 0
        self.cnt_mpc = 0
        self.plot = False
        self.metrics = 'none' #standard, fast

        self.min_thrust = 880 * 1000 #N
        self.max_thrust = 1 * 2210 * 1000 #kN

        deg_to_rad = 0.01745329252

        self.max_gimble = 20 * deg_to_rad
        self.min_gimble = self.max_gimble

        with open('./data/data_mpc.pkl', 'rb') as file:
            self.mpc_values = pickle.load(file)
        file.close()

        self.a_model = pickle.load(open('./data/angle_model.pkl', 'rb'))
        self.t_model = pickle.load(open('./data/thrust_model.pkl','rb'))

        self.thrust_optm = thrust_optm
        self.angle_optm =  angle_optm

        # create metrics db
        try:
            self.df = pd.read_pickle('./mpc_history.pkl')
            if self.metrics == 'fast':
                self.plot_metrics()
        except:
            self.df = pd.DataFrame()

    async def filtered_sensor_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def transform_action(self, transformed_obs, action):
        if type(transformed_obs) != dict:
            X = transformed_obs
        else:
            if 'observation' in transformed_obs.keys():
                X = [transformed_obs['observation']]
            else:
                X = pd.DataFrame(data=[[float(transformed_obs['x']), float(transformed_obs['x_speed']), float(transformed_obs['y']),
                float(transformed_obs['y_speed']), float(transformed_obs['angle']), float(transformed_obs['ang_speed'])]],
                columns=['x_obs','x_speed', 'y_obs', 'y_speed', 'angle', 'ang_speed'])



        if self.count == 0:
            t = self.thrust_optm[self.count] - 0
            a = self.angle_optm[self.count] - 0
        else:
            t = self.thrust_optm[self.count] - self.thrust_optm[self.count-1]
            a = self.angle_optm[self.count] - self.angle_optm[self.count-1]

        #t = self.t_model.predict(X)[0] + action[1]
        #a = self.a_model.predict(X)[0] + action[0]
        t = action[1]
        a = action[0]

        action = [a, t]
        print('Action: ', action)
        #print('MPC: ', [self.thrust_optm[self.count], self.angle_optm[self.count]])
        #action = [self.mpc_values['angle'][self.cnt_mpc+1],self.mpc_values['angle'][self.cnt_mpc+1]]
        return action

    async def filtered_observation_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        #r1 = (float(transformed_obs["angle"]) - self.mpc_values['angle'][self.cnt_mpc+1])**2
        #r2 = (float(transformed_obs["ang_speed"]) - self.mpc_values['angle_speed'][self.cnt_mpc+1])**2
        #r3 = (float(transformed_obs["x"]) - self.mpc_values['x'][self.cnt_mpc+1])**2
        #r4 = (float(transformed_obs["x_speed"]) - self.mpc_values['x_speed'][self.cnt_mpc+1])**2
        #r5 = (float(transformed_obs["y"]) - self.mpc_values['y'][self.cnt_mpc+1])**2
        #r6 = (float(transformed_obs["y_speed"]) - self.mpc_values['y_speed'][self.cnt_mpc+1])**2

        #reward_mimic = float(1/ ((r1 + r2 + r3 + r4 + r5 + r6)))

        error_1 = ((0 - float(transformed_obs["x"]) )/400)**2
        error_2 = ((0 - float(transformed_obs["x_speed"]))/100)**2
        error_3 = ((0 - float(transformed_obs["y"]) )/1000)**2
        error_4 = ((0 - float(transformed_obs["y_speed"]))/100)**2
        error_5 = ((0 - float(transformed_obs["angle"]))/3.15)**2
        error_6 = ((0 - float(transformed_obs["ang_speed"]))/1)**2

        reward_goal = (1000 - float(transformed_obs["y"])) * (1/(5 * error_1 + 1 * error_2 + 1 * error_3 + 5 * error_4 + 5 * error_5 + 3 * error_6))

        #reward = float(1e3*reward_mimic + 0.01*reward_goal)

        #reward = reward_mimic

        #print('REWARDS: ',reward, 1e5*reward_mimic, 0.01*reward_goal)
        #self.t += action[0]
        #self.a += action[1]
        self.t = action[1]
        self.a = action[0]

        #self.t = np.clip(self.t,0.4,1)
        #self.t = np.clip(self.t, self.min_thrust, self.max_thrust)
        #self.a = np.clip(self.a, -self.max_gimble, self.max_gimble)
        #self.a = np.clip(self.a, self.min_gimble, self.max_gimble)
        #print('action: ', [self.t, self.a])
        #print('MPC: ', [self.thrust_optm[self.count], self.angle_optm[self.count]])

        self.action_history.append(action)
        self.thrust_history.append([self.t, self.a])

        ######### REWARD
        #self.t_error = (self.t - self.mpc_values['thrust'][self.cnt_mpc+1])**2
        self.t_error = (self.t - self.thrust_optm[self.count])**2
        self.a_error = (self.a - self.angle_optm[self.count])**2

        reward_action = (math.e ** (-self.t_error)) + (math.e ** (-self.a_error))
        self.error_history.append(self.t_error + 100*self.a_error)
        rms = np.mean(self.error_history)
        #reward_action = 1/(self.t_error + self.a_error + 1e-5)
        reward_action = (1e-3/(rms + 1e-5))
        reward_action = math.exp(-1e-1 * np.sum(self.error_history))
        #reward_action = 1/self.a_error
        #reward_action = 10* (1/(self.t_error + self.a_error))

        reward_goal = math.exp(-0.1* (5 * error_1 + 1 * error_2 + 1 * error_3 + 5 * error_4 + 5 * error_5 + 3 * error_6))
        #print('REWARDS: ', reward_action, reward_goal)
        reward = 0.8 * reward_action + 0.2 * reward_goal
        reward = reward_action
        reward = float(reward)

        self.reward_history.append(reward)
        self.angle_history.append(transformed_obs['angle'])
        self.count += 1
        self.cnt_mpc += 1
        # history metrics
        df_temp = pd.DataFrame(columns=['time','x','y','x_speed', 'y_speed', 'angle', 'angle_speed','reward'],
                               data=[[self.count,transformed_obs['x'], transformed_obs['y'],transformed_obs['x_speed'], transformed_obs['y_speed'],
                                      transformed_obs['angle'], transformed_obs['ang_speed'], reward]])
        self.df = pd.concat([self.df, df_temp])
        self.df.to_pickle("./history/mpc_history.pkl")

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        if self.plot:
            if len(self.obs_history) > 100 and len(self.obs_history) % 10 == 100:
                self.plot_obs('Rocket Landing')

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

    async def compute_termination(self, transformed_obs, action):
        if self.count >= 398:
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


class DRLHighSkillTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.action_history = []
        self.thrust_history = []
        self.angle_history = []
        self.error_history = []
        self.t = 0.4
        self.a = -3.14/2

        self.t = 0.0
        self.a = 0.0

        self.count = 0
        self.cnt_mpc = 0
        self.plot = False
        self.metrics = 'none' #standard, fast

        self.min_thrust = 880 * 1000 #N
        self.max_thrust = 1 * 2210 * 1000 #kN

        deg_to_rad = 0.01745329252

        self.max_gimble = 20 * deg_to_rad
        self.min_gimble = self.max_gimble

        with open('./data/data_mpc.pkl', 'rb') as file:
            self.mpc_values = pickle.load(file)
        file.close()

        self.a_model = pickle.load(open('./data/angle_model.pkl', 'rb'))
        self.t_model = pickle.load(open('./data/thrust_model.pkl','rb'))

        self.thrust_optm = thrust_optm
        self.angle_optm =  angle_optm

        # create metrics db
        try:
            self.df = pd.read_pickle('./mpc_history.pkl')
            if self.metrics == 'fast':
                self.plot_metrics()
        except:
            self.df = pd.DataFrame()

    async def filtered_sensor_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_observation_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        reward = 0.0

        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        success = False
        return success

    async def compute_termination(self, transformed_obs, action):
        return False
