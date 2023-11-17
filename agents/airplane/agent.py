import os

from composabl import Agent, Runtime, Scenario, Skill
from teacher import NavigationTeacher
from sensors import sensors

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def start():
    Navigation_scenarios = [
        {
            "y1": 0,
            "y2": 0,
            "u1": 0,
            "u2": 0,
            "u3": 0,
            "u4": 0
        }
    ]

    Navigation_skill = Skill("Navigation", NavigationTeacher, trainable=True)

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-airplane"
            },
            #"local": {
            #   "address": "localhost:1337"
            #}
        },
        "env": {
            "name": "airplane",
        },
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(Navigation_skill)

    try:
        files = os.listdir(PATH_CHECKPOINTS)

        if '.DS_Store' in files:
            files.remove('.DS_Store')

        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    agent.train(train_iters=10)

    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
