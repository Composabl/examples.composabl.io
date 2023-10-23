import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from teacher import CSTRTeacher

from cstr.external_sim.sim import CSTREnv
import pandas as pd

license_key = os.environ["COMPOSABL_KEY"]


def start():
    # delete old history files
    dir = './cstr/deep_reinforcement_learning'
    files = os.listdir(dir)
    pkl_files = [file for file in files if file.endswith('.pkl')]
    for file in pkl_files:
        file_path = os.path.join(dir, file)
        os.remove(file_path)
        
    T = Sensor("T", "")
    Tc = Sensor("Tc", "")
    Ca = Sensor("Ca", "")
    Cref = Sensor("Cref", "")
    Tref = Sensor("Tref", "")

    sensors = [T, Tc, Ca, Cref, Tref]

    # Cref_signal is a configuration variable for Concentration and Temperature setpoints
    reaction_scenarios = [
        {
            "Cref_signal": "complete"
        }
    ]

    reaction_skill = Skill("reaction", CSTRTeacher, trainable=True)
    for scenario_dict in reaction_scenarios:
        reaction_skill.add_scenario(Scenario(scenario_dict))

    config = {
        "license": license_key,
        "target": {
            "local": {
            "address": "localhost:1337"
            }
        },
        "env": {
            "name": "sim-cstr",
        },

        "flags": {
            "print_debug_info": True
        },
}
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    checkpoint_path = './cstr/deep_reinforcement_learning/saved_agents/'

    #load agent
    agent.load(checkpoint_path)
    agent.train(1)

    #save agent
    trained_agent = agent.prepare()

    # Inference
    sim = CSTREnv()
    sim.scenario = Scenario(reaction_scenarios[0])
    df = pd.DataFrame()
    obs, info= sim.reset()
    for i in range(90):
        action = trained_agent.execute(obs)
        obs, reward, done, truncated, info = sim.step(action)
        df_temp = pd.DataFrame(columns=['T','Tc','Ca','Cref','Tref','time'],data=[list(obs) + [i]])
        df = pd.concat([df, df_temp])

        if done:
            break
    
    # save history data
    df.to_pickle("./cstr/deep_reinforcement_learning/inference_data.pkl")  

if __name__ == "__main__":
    start()
