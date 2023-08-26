import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from .teacher import (AlignmentTeacher, NavigationTeacher, SpeedControlTeacher,
                      StabilizationTeacher)

license_key = os.environ["COMPOSABL_KEY"]


def selector(x, y, angle, angle_speed):
    if abs(x) > 100 or y > 500:
        return "Navigation_skill"

    elif abs(angle) > 0.1 or abs(angle_speed) > 0.1:
        return "Stabilization_skill"

    elif y > 100:
        return "Alignment_skill"

    else:
        return "SpeedControl_skill"


def start():
    print("composabl_core|====================================================================")
    print("composabl_core|")
    print("composabl_core|Running the Starship Agent")

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

    Navigation_skill = Skill("Navigation", NavigationTeacher, trainable=True)
    Alignment_skill = Skill("Alignment", AlignmentTeacher, trainable=True)
    SpeedControl_skill = Skill("SpeedControl", SpeedControlTeacher, trainable=True)
    Stabilization_skill = Skill("Stabilization", StabilizationTeacher, trainable=True)
    #selector_skill = Skill("selector", Navigation_reward(), trainable=True) #using the same reward

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)
        Alignment_skill.add_scenario(scenario)
        SpeedControl_skill.add_scenario(scenario)
        Stabilization_skill.add_scenario(scenario)
        # selector_skill.add_scenario(scenario)

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

    agent.add_skill(Navigation_skill)
    agent.add_skill(Alignment_skill)
    agent.add_skill(SpeedControl_skill)
    agent.add_skill(Stabilization_skill)
    # agent.add_selector_skill(selector_skill, [Navigation_skill, Alignment_skill], fixed_order=True, repeat=False)

    agent.train(train_iters=5)
