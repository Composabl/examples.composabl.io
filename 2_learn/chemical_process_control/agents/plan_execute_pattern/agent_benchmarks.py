import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from chemical_process_control.agents.config import config
from chemical_process_control.agents.sensors import sensors
from chemical_process_control.sim.src.sim import CSTREnv
from composabl import Agent, Scenario, Skill, Trainer
from teacher import CSTRTeacher

license_key = os.environ["COMPOSABL_LICENSE"]

# Cref_signal is a configuration variable for Concentration and Temperature setpoints
control_scenarios = [
    {
        "Cref_signal": "complete",
        "noise_percentage": 0.0
    }
]

control_skill = Skill("control", CSTRTeacher)
for scenario_dict in control_scenarios:
    control_skill.add_scenario(Scenario(scenario_dict))

trainer = Trainer(config)
agent = Agent()
agent.add_sensors(sensors)

agent.add_skill(control_skill)

checkpoint_path = './cstr/skill_group_drl_mpc/saved_agents/'

#load agent
agent.load(checkpoint_path)

#save agent
trained_agent = trainer.package(agent)

noise = 0.05
sim = CSTREnv()
sim.scenario = Scenario({
        "Cref_signal": "complete",
        "noise_percentage": noise
    })

df = pd.DataFrame()

for i in range(30):
    # Inference
    obs, info = sim.reset()
    for i in range(90):
        action = trained_agent.execute(obs)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break


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

plt.savefig('./cstr/skill_group_drl_mpc/benchmark_figure.png')
