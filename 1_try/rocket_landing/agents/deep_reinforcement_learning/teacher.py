import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Teacher
from composabl_core.agent.skill.goals import CoordinatedGoal, MaintainGoal, ApproachGoal,  GoalCoordinationStrategy
from sensors import sensors
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, rc
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from ipywidgets import IntProgress
from IPython.display import display
import math
import numpy as np
import pandas as pd

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

class NavigationTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.count = 0
        self.t = 0
        self.a = 0
        self.action_history = []
        self.thrust_history = []
        self.reward_history = []
        self.angle_history = []
        self.error_history = []

        self.plot = False
        self.metrics = 'fast' #standard, fast

        #if self.plot:
        #    plt.close("all")
        #    plt.figure(figsize=(10,7))
        #    plt.ion()

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
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        error_1 = ((0 - float(transformed_obs["x"]) )/400)**2
        error_2 = ((0 - float(transformed_obs["x_speed"]))/100)**2
        error_3 = ((0 - float(transformed_obs["y"]) )/1000)**2
        error_4 = ((5 - float(transformed_obs["y_speed"]))/1000)**2
        error_5 = ((0 - float(transformed_obs["angle"]))/3.15)**2
        error_6 = ((0 - float(transformed_obs["ang_speed"]))/1)**2

        reward = (1000 - float(transformed_obs["y"])) * (1/(5 * error_1 + 1 * error_2 + 1 * error_3 + 5 * error_4 + 5 * error_5 + 3 * error_6))

        self.t = action[1]
        self.a = action[0]
        deg_to_rad = 0.01745329

        max_gimble = 20  * deg_to_rad
        min_gimble = -max_gimble
        #self.t = np.clip(self.t,0.4,1)
        self.a = np.clip(self.a, min_gimble, max_gimble)

        ##################
        error = (1000 - float(transformed_obs["y"])) * (5 * error_1 + 1 * error_2 + 1 * error_3 + 5 * error_4 + 5 * error_5 + 3 * error_6)
        error = (5 * error_1 + 1 * error_2 + 1 * error_3 + 5 * error_4 + 5 * error_5 + 1 * error_6)
        self.error_history.append(error)
        rms = math.sqrt(np.mean(self.error_history))
        # minimize error
        reward = 10* math.exp(-1e-1 * np.sum(self.error_history))
        if len(self.error_history) >= 10:
            #print('LEN HISTORY: ', self.error_history)
            reward = 10* math.exp(-1e-1 * np.sum(self.error_history[-10:]))
        self.reward_history.append(reward)

        ##############

        self.action_history.append(action)
        self.thrust_history.append([self.t, self.a])
        self.reward_history.append(reward)
        self.angle_history.append(transformed_obs['angle'])

        self.count += 1

        # history metrics
        #df_temp = pd.DataFrame(columns=['time','x','y','x_speed', 'y_speed', 'angle', 'angle_speed','reward'],
        #                       data=[[self.count,transformed_obs['x'], transformed_obs['y'],transformed_obs['x_speed'], transformed_obs['y_speed'],
        #                              transformed_obs['angle'], transformed_obs['ang_speed'], reward]])
        #self.df = pd.concat([self.df, df_temp])
        #self.df.to_pickle("./starship/history.pkl")
        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history == None:
            return False
        else:
            success = False

            if self.plot:
                if len(self.obs_history) > 100 and len(self.obs_history) % 100 == 0:
                    self.plot_obs('Stabilization')

            if self.metrics == 'standard':
                try:
                    self.plot_metrics()
                except Exception as e:
                    print('Error: ', e)

            return success

    async def compute_termination(self, transformed_obs, action):
        if abs(float(transformed_obs["x"])) > 150:
            return True
        elif (float(transformed_obs["x_speed"])) < -100:
            return True
        elif abs(float(transformed_obs["angle"])) > 2.5:
            return True
        else:
            return False

    async def plot_metrics(self):
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

        #plt.show()
        plt.draw()
        plt.pause(0.001)

    async def plot_obs(self, title='Starship'):
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


class GoalTeacher(CoordinatedGoal):
    def __init__(self, *args, **kwargs):
        navigationx_goal = MaintainGoal("x", "Drive x coordinate to center", target=0, stop_distance=5)
        navigationy_goal = ApproachGoal("y", " ", target=0, stop_distance=0.1)
        angle_goal = MaintainGoal("angle", " ", target=0, stop_distance=0.01)
        y_speed_goal = MaintainGoal("y_speed", " ", target=2, stop_distance=2)

        super().__init__([navigationx_goal, angle_goal, y_speed_goal, navigationy_goal], GoalCoordinationStrategy.AND)

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        return action

    async def filtered_sensor_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        if abs(float(transformed_obs["angle"])) > 2:
            return True
        else:
            return False


class LandTeacher(Teacher):
    def __init__(self, *args, **kwargs):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0
        self.count = 0
        self.t = 0
        self.a = 0
        self.action_history = []
        self.thrust_history = []
        self.reward_history = []
        self.angle_history = []
        self.error_history = []

    async def transform_sensors(self, obs, action):
        return obs

    async def transform_action(self, transformed_obs, action):
        #constraint delta action
        '''if self.count > 1:
            last_t = self.action_history[-1][0]
            last_a = self.action_history[-1][1]
            delta_t = action[0] - last_t
            delta_a = action[1] - last_a

            delta_t = np.clip(delta_t, -0.1, 0.1)
            delta_a = np.clip(delta_a, -0.1, 0.1)

            action = [last_t + delta_t, last_a + delta_a]'''
        return action

    async def filtered_sensor_space(self):
        return ['x', 'x_speed', 'y', 'y_speed', 'angle', 'ang_speed']

    async def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0.0
        else:
            self.obs_history.append(transformed_obs)

        # dist between agent and target point
        self.target_x = 0
        self.target_y = 0
        dist_x = abs(transformed_obs['x'] - self.target_x)
        dist_y = abs(transformed_obs['y'] - self.target_y)
        dist_norm = dist_x / 400 + dist_y / 1000

        dist_reward = 0.1*(1.0 - dist_norm)

        if abs(transformed_obs['angle']) <= np.pi / 6.0:
            pose_reward = 0.1
        else:
            pose_reward = abs(transformed_obs['angle']) / (0.5*np.pi)
            pose_reward = 0.1 * (1.0 - pose_reward)

        reward = 10 * (dist_reward + pose_reward)

        '''if self.task == 'hover' and (dist_x**2 + dist_y**2)**0.5 <= 2*self.target_r:  # hit target
            reward = 0.25
        if self.task == 'hover' and (dist_x**2 + dist_y**2)**0.5 <= 1*self.target_r:  # hit target
            reward = 0.5
        if self.task == 'hover' and abs(transformed_obs['angle']) > 90 / 180 * np.pi:
            reward = 0'''

        v = (transformed_obs['x_speed'] ** 2 + transformed_obs['y_speed'] ** 2) ** 0.5

        '''if self.already_crash:
            reward = (reward + 5*np.exp(-1*v/10.)) * (self.max_steps - self.step_id)
        if self.already_landing:
            reward = (1.0 + 5*np.exp(-1*v/10.))*(self.max_steps - self.step_id)'''

        ##### Landing zone
        # x value
        if float(transformed_obs['y']) <= 200 and abs(float(transformed_obs['x'])) <= 100:
            reward += 0.1
        if float(transformed_obs['y']) <= 200 and abs(float(transformed_obs['x'])) <= 50:
            reward += 0.5
        if float(transformed_obs['y']) <= 200 and abs(float(transformed_obs['x'])) <= 10:
            reward += 1

        # angle
        if float(transformed_obs['y']) <= 600 and abs(float(transformed_obs['angle'])) <= 1:
            reward += 0.1
        if float(transformed_obs['y']) <= 400 and abs(float(transformed_obs['angle'])) <= 0.4:
            reward += 0.5
        if float(transformed_obs['y']) <= 200 and abs(float(transformed_obs['angle'])) <= 0.4:
            reward += 0.5
        if float(transformed_obs['y']) <= 200 and abs(float(transformed_obs['angle'])) <= 0.2:
            reward += 1
        if float(transformed_obs['y']) <= 100 and abs(float(transformed_obs['angle'])) <= 0.2:
            reward += 5

        # speed
        if float(transformed_obs['y']) <= 400 and abs(float(transformed_obs['y_speed'])) < 100:
            reward += 0.1
        if float(transformed_obs['y']) <= 200 and abs(float(transformed_obs['y_speed'])) < 80:
            reward += 0.5
        if float(transformed_obs['y']) <= 100 and abs(float(transformed_obs['y_speed'])) < 50:
            reward += 1.0
        if float(transformed_obs['y']) <= 20 and abs(float(transformed_obs['y_speed'])) <= 10:
            reward += 10
        if float(transformed_obs['y']) <= 10 and abs(float(transformed_obs['y_speed'])) <= 5:
            reward += 10

        self.reward_history.append(reward)

        ##############

        self.action_history.append(action)
        self.thrust_history.append([self.t, self.a])
        self.reward_history.append(reward)
        self.angle_history.append(transformed_obs['angle'])

        self.count += 1

        # history metrics
        #df_temp = pd.DataFrame(columns=['time','x','y','x_speed', 'y_speed', 'angle', 'angle_speed','reward'],
        #                       data=[[self.count,transformed_obs['x'], transformed_obs['y'],transformed_obs['x_speed'], transformed_obs['y_speed'],
        #                              transformed_obs['angle'], transformed_obs['ang_speed'], reward]])
        #self.df = pd.concat([self.df, df_temp])
        #self.df.to_pickle("./starship/history.pkl")
        return reward

    async def compute_action_mask(self, transformed_obs, action):
        return None

    async def compute_success_criteria(self, transformed_obs, action):
        if self.obs_history == None:
            return False
        else:
            success = False
        return success

    async def compute_termination(self, transformed_obs, action):
        if abs(float(transformed_obs["x"])) > 150:
            return True
        elif (float(transformed_obs["x_speed"])) < -100:
            return True
        elif abs(float(transformed_obs["angle"])) > 2.5:
            return True
        elif abs(float(transformed_obs["y"])) < 400 and abs(float(transformed_obs["angle"])) > 1.0:
            return True
        else:
            return False
