import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import random
from sensors import sensors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from composabl import SkillController


def PID(TPV,
        TSP,
        Kp,
        Ki,
        Kd,
        TauI,
        TauD,
        Tkm1,
        dt = 1,
        Ubias = 0,
        I = 0,
        N = 10,
        b = 1,
        c = 0,
        Method = 'Backward'):

    e = TSP - TPV
    e_anterior = TSP - Tkm1
    print('erros: ',e, e_anterior)
    Ti = TauI
    Td = TauD

    if Method == 'Backward':
        b1 = Kp * dt / Ti if Ti != 0 else 0.0
        b2 = 0.0
        ad = Td / (Td + N * dt)
        bd = Kp * Td * N / (Td + N * dt)

    elif Method == 'Forward':
        b1 = 0.0
        b2 = Kp * dt / Ti  if Ti != 0 else 0.0
        ad = 1 - N * dt / Td if Td != 0 else 0.0
        bd = Kp * N

    elif Method == 'Tustin':
        b1 = Kp * dt / 2 / Ti if Ti != 0 else 0.0
        b2 = b1
        ad = (2 * Td - N * dt) / (2 * Td + N * dt)
        bd = 2 * Kp * Td * N / (2 * Td + N * dt)

    elif Method == 'Ramp':
        b1 = Kp * dt / 2 / Ti if Ti != 0 else 0.0
        b2 = b1
        ad = np.exp(-N * dt / Td) if Td != 0 else 0.0
        bd = Kp * Td * (1 - ad) / dt

    P = e
    P = Kp * (b * e)
    # Integral action:
    I = e*dt + I
    I = b1 * (e) + b2 * (e_anterior)
    # Derivative Action:
    D = (e-e_anterior)/dt
    D_int = 0
    D  = ad * D_int + bd * ((c * e) - (c * e_anterior))

    #U = U0 + Kp*(P + (1/TauI)*I + TauD*D)
    #U = U0 + Kp + Ki*I + Kd*D
    U = Ubias + P + I + D

    #print(U)

    return U


PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"

class PIDController(SkillController):
    def __init__(self, *args, **kwargs):
        #initialize variables
        self.count = 0
        self.Δu1 = 0
        self.y1_list = [0]
        self.y1ref = 0
        self.y1 = 0
        self.I = 0

    async def compute_action(self, obs, action):
        self.y1ref = obs[1]
        self.y1 = obs[0]
        bias = 0

        if self.count > 0:
            self.Δu1 = PID(self.y1,TSP=self.y1ref,Kp=0.3, Ki=0.07, Kd =0.1,
                        TauI=0.78,TauD=0.5,
                        Tkm1=self.y1_list[0][self.cnt-2],dt=1,Ubias=bias, I=self.I, N=1) #Kp=0.3 , 0.78, 0.5 (0.6,0.78)

        self.y1_list.append(obs[0])

        self.count += 1
        return [self.Δu1]

    async def transform_sensors(self, obs):
        return obs

    async def filtered_sensor_space(self):
        return [s.name for s in sensors]

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False
