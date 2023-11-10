import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import CSTRTeacher

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def start():
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]
        for file in pkl_files:
            file_path = os.path.join(dir, file)
            os.remove(file_path)
    except:
        pass

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
            }
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "workers": 8
        }
    }

    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(reaction_skill)

    try:
        files = os.listdir(PATH_CHECKPOINTS)

        if '.DS_Store' in files:
            files.remove('.DS_Store')

        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    agent.train(train_iters=20)
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
