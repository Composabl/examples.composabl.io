import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from composabl_core.grpc.client.client import make

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.cleanup import clean_folder
from utils.config import generate_config

license_key = os.environ["COMPOSABL_LICENSE"]
PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

DOCKER_IMAGE: str = "composabl/sim-cstr:latest"

config = generate_config(
    license_key=license_key,
    target="docker",
    image=DOCKER_IMAGE,
    env_name="sim-cstr",
    workers=1,
    num_gpus=0,
)

# Remove unused files from path (mac only)
clean_folder(PATH_CHECKPOINTS, ".DS_Store")

# Start Runtime
runtime = Runtime(config)
directory = PATH_CHECKPOINTS

# Load the pre trained agent
agent = Agent.load(directory)

# Prepare the loaded agent for inference
trained_agent = runtime.package(agent)

# Inference
print("Creating Environment")
sim = make(
    "run-benchmark",
    "sim-benchmark",
    "",
    "localhost:1337",
    {
        "render_mode": "rgb_array"
    },
)

print("Initializing Environment")
sim.init()
print("Initialized")

noise = 0.05
sim.set_scenario(Scenario({
        "Cref_signal": "complete",
        "noise_percentage": noise
    }))
df = pd.DataFrame()

for i in range(100):
    obs, info= sim.reset()
    for i in range(90):
        action = trained_agent.execute(obs)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break

print("Closing")
sim.close()


# calculate error
df['error_temp'] = (df['T'] - df['Tref'])**2
df['error_conc'] = (df['Ca'] - df['Cref'])**2
rmsT = round(np.sqrt(np.mean(df['error_temp'])),2)
rmsCa = round(np.sqrt(np.mean(df['error_conc'])),2)
print('RMS T: ', rmsT)
print('RMS Ca: ', rmsCa)

plt.subplot(2,1,1)
Tr_list_ = df.set_index('time')['T']
Tref_list = df.set_index('time')['Tref'][:90]
min_Tr = [min(np.array(Tr_list_[i])) for i in range(90)]
max_Tr = [max(np.array(Tr_list_[i])) for i in range(90)]
mean_Tr = [np.mean(np.array(Tr_list_[i])) for i in range(90)]
plt.fill_between([i for i in range(90)] , min_Tr , max_Tr, alpha = 0.2)
plt.plot([i for i in range(90)],Tref_list,'k--',lw=2,label=r'$T_{sp}$')
plt.plot([i for i in range(90)],mean_Tr,'b.-',lw=1,label=r'$T_{sp}$')
plt.plot([i for i in range(90)],[400 for x in range(90)],'r--',lw=1)
plt.ylabel('Temperature')
plt.title(f'Benchmarks Noise: {noise}' + f" (RMS T: {rmsT} , RMS Ca: {rmsCa})")

plt.subplot(2,1,2)
Cr_list_ = df.set_index('time')['Ca']
Cref_list = df.set_index('time')['Cref'][:90]
min_Cr = [min(np.array(Cr_list_[i])) for i in range(90)]
max_Cr = [max(np.array(Cr_list_[i])) for i in range(90)]
mean_Cr = [np.mean(np.array(Cr_list_[i])) for i in range(90)]
plt.fill_between([i for i in range(90)] , min_Cr , max_Cr, alpha = 0.2)
plt.plot([i for i in range(90)],Cref_list,'k--',lw=2,label=r'$C_{sp}$')
plt.plot([i for i in range(90)],mean_Cr,'b.-',lw=1,label=r'$C_{sp}$')
plt.ylabel('Concentration')

plt.savefig(f"{PATH}/img/benchmark_figure.png")
