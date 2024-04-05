import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from teacher import (DRLMPCTeacher)

license_key = os.environ["COMPOSABL_KEY"]


def start():
    # delete old history files
    dir = './starship'
    files = os.listdir(dir)
    pkl_files = [file for file in files if file.endswith('.pkl')]
    for file in pkl_files:
        file_path = os.path.join(dir, file)
        os.remove(file_path)

    x = Sensor("x", "")
    x_speed = Sensor("x_speed", "")
    y = Sensor("y", "")
    y_speed = Sensor("y_speed", "")
    angle = Sensor("angle", "")
    ang_speed = Sensor("ang_speed", "")

    sensors = [x, x_speed, y, y_speed, angle, ang_speed]

    Navigation_scenarios = [
        {
            "x": 0,
            "x_speed": 0,
            "y": 1000,
            "y_speed": -80,
            "angle": -3.14 / 2,
            "ang_speed": 0
        }
    ]

    mpc_skill = Skill('mpc', DRLMPCTeacher, trainable=True)

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        mpc_skill.add_scenario(scenario)

    config = {
        "env": {
            "name": "starship",
            "compute": "local",  # "docker", "kubernetes", "local"
            "strategy": "local",  # "docker", "kubernetes", "local"
            "config": {
                "address": "localhost:1337",
                # "image": "composabl.ai/sim-gymnasium:latest"
            }
        },
        "license": license_key,
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(mpc_skill)

    agent.train(train_iters=20)


if __name__ == "__main__":
    start()
