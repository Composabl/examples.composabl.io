import math
import random
import numpy as np
from scipy import interpolate

from composabl_core.agent.scenario import Scenario
import gymnasium as gym

from cstr_sim import cstr_model as cstr


class CSTREnv(gym.Env):
    def __init__(self, *args, **kwargs):
        """
        actions = 1 : dTc (delta coolant temperature)
        sensor_variables = 5 :
            T (Temperature - K)
            Tc (Coolant temperature - K)
            Ca (Product Concentration (A) - kmol/m3)
            Cref (Product Concentration Reference (SetPoint)  - kmol/m3 )
            Tref (Temperature Reference (SetPoint) - K)
            Concentratio_Error (Ca - Cref)
            Episode Yield Percentage (% of time that the product is in spec)
            Production Cb Total (Total of Cb produced)
        Cref_signal:
            1 - transition
            2 - ss1 - steady state 1 only
            3 - ss2 - steady state 2 only
            4 - complete
        """
        self.Cref_signal = "complete"
        self.noise_percentage = 0
        self.count = 0
        self.T = 0
        self.concentration_error = 0
        self.tolerance = 0
        self.episode_yield_pct = 0
        self.production_Cb_total = 0
        self.obs_history = []
        self.y_list = []
        self.error_list = []
        self.scenario = None

        self.observation_space = gym.spaces.Box(
            low=np.array([200, 200, 0, 0, 200, 0, 0, 0]), high=np.array([500, 500, 12, 12, 500, 100, 1, 1000])
        )
        self.action_space = gym.spaces.Box(low=np.array([-10.0]), high=np.array([10.0]))


    def reset(self):
        # initial conditions
        Ca0: float = 8.5698  # kmol/m3
        T0: float = 311.2639  # K
        Tc0: float = 292  # K

        self.T = T0
        self.Tc = Tc0
        self.Ca = Ca0
        self.ΔTc = 0
        self.tolerance = 0.5
        self.Cref = 8.5698
        self.Tref = 311.2612

        # Define scenario in the simulation
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])

        noise_percentage = self.noise_percentage

        # time counter
        self.count = 0

        self.noise_percentage = noise_percentage
        # validation, if someone sends a noise not in the {0,1} format assume that they sent in pct values
        if self.noise_percentage > 1:
            self.noise_percentage = self.noise_percentage / 100

        '''if self.Cref_signal == "ss1":
            self.Cref = 2
            self.Tref = 373.1311
        else:
            self.Cref = 8.5698
            self.Tref = 311.2612'''

        # Detect the Cref signal from scenarios
        if self.Cref == 2 and self.Tref == 373.1311 and self.count == 0:
            self.Cref_signal = "ss2"
        elif self.Cref == 8.5698 and self.Tref == 311.2612 and self.count == 0:
            self.Cref_signal = "ss1"
        elif self.Cref == 8.5698 and self.Tref == 311.2612 and self.count > 1:
            self.Cref_signal = "transition"
        else:
            self.Cref_signal = "complete"

        self.rms = 0
        self.obs_history = []
        self.y_list = []
        self.error_list = []
        self.obs = np.array([self.T, self.Tc, self.Ca, self.Cref, self.Tref, self.concentration_error, self.episode_yield_pct, self.production_Cb_total])
        info = {}
        return self.obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        action = float(action[0])
        if self.count >= 90:
            self.count = 90
        if self.Cref_signal == "transition":
            # update Cref an Tref
            time = 90
            p1 = 22
            p2 = 74
            k = self.count + p1
            C = interpolate.interp1d([0, p1, p2, time], [8.57, 8.57, 2, 2])
            self.Cref = float(C(k))
            T_ = interpolate.interp1d([0, p1, p2, time], [311.2612, 311.2612, 373.1311, 373.1311])
            self.Tref = float(T_(k))
        elif self.Cref_signal == "ss1":
            self.Cref = 2
            self.Tref = 373.1311
        elif self.Cref_signal == "ss2":
            self.Cref = 8.5698
            self.Tref = 311.2612
        elif self.Cref_signal == "complete":
            k = self.count
            time = 90
            # update Cref an Tref
            p1 = 22
            p2 = 74
            C = interpolate.interp1d([0, p1, p2, time], [8.57, 8.57, 2, 2])
            self.Cref = float(C(k))
            T_ = interpolate.interp1d([0, p1, p2, time], [311.2612, 311.2612, 373.1311, 373.1311])
            self.Tref = float(T_(k))

        self.ΔTc = action

        error_var = self.noise_percentage
        σ_max1 = error_var * (8.5698 - 2)
        σ_max2 = error_var * (373.1311 - 311.2612)

        σ_Ca = random.uniform(-σ_max1, σ_max1)
        σ_T = random.uniform(-σ_max2, σ_max2)

        self.ΔTc = np.clip(self.ΔTc, -10, 10)

        # calling the CSTR python model
        sim_model = cstr.CSTRModel(T=self.T, Ca=self.Ca, Tc=self.Tc, ΔTc=self.ΔTc)

        # Tc
        self.Tc += self.ΔTc
        self.Tc = np.clip(self.Tc, 200, 500)

        # Tr
        self.T = sim_model.T + σ_T

        # Ca
        self.Ca = sim_model.Ca + σ_Ca
        self.y_list.append(self.Ca)

        self.obs_history.append([self.Ca,self.Cref])

        # Increase time counter
        self.count += 1

        # Error and Reward
        error = (self.Ca - self.Cref)**2
        self.error_list.append(error)
        self.rms = math.sqrt(sum(self.error_list) / len(self.error_list))

        # instataneous yield regardless of time, it has to be in spec
        yield_inst = 1 if abs(self.Ca - self.Cref) <= self.tolerance else 0
        # yield percentage over the episode - % time that the product is in spec
        self.episode_yield_pct = sum([ 1 if abs(x[0] - x[1]) <= self.tolerance else 0 for x in self.obs_history]) / len(self.obs_history)
        #product needs to be in spec after 76 iterations to produce yield
        product_Cb_inst = (10 - float(self.Ca)) if (self.count >= 76 and abs(self.Ca - self.Cref) <= self.tolerance) else 0
        self.production_Cb_total = sum([ (10 - x[0]) if abs(x[0] - x[1]) <= self.tolerance else 0 for x in self.obs_history])

        self.concentration_error = error

        #REWARD
        if self.T >= 400 :  # avoid
            reward = float(-10)
        else:
            reward = float(1 / self.rms)

        done = False

        # Constraints to break the simulation
        if self.count == 90 or (self.Cref_signal == "transition" and self.count == 68):
            done = True

        info = {}

        self.obs = np.array([self.T, self.Tc, self.Ca, self.Cref, self.Tref, self.concentration_error, self.episode_yield_pct, self.production_Cb_total])
        return self.obs, reward, done, False, info

    def render(self, mode='human', close=False):
        print("render")
