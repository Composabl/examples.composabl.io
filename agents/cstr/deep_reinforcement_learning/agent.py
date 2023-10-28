import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from teacher import CSTRTeacher

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
            "docker": {
                "image": "composabl/sim-cstr:latest"
            },
            #"local": {
            #"address": "localhost:1337"
            #}
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "ray": {
                "workers": 1
            }
        }
    }

    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    checkpoint_path = './cstr/deep_reinforcement_learning/saved_agents/'

    files = os.listdir(checkpoint_path)
    if '.DS_Store' in files:
        files.remove('.DS_Store')

    if len(files) > 0:
        #load agent
        agent.load(checkpoint_path)

    agent.train(train_iters=100)

    #save agent
    agent.export(checkpoint_path)


if __name__ == "__main__":
    start()
