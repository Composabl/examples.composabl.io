import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from teacher import (AlignmentTeacher, NavigationTeacher, SpeedControlTeacher,
                     StabilizationTeacher)

license_key = os.environ["COMPOSABL_LICENSE"]


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

    Navigation_skill = Skill("Navigation", NavigationTeacher)
    Alignment_skill = Skill("Alignment", AlignmentTeacher)
    SpeedControl_skill = Skill("SpeedControl", SpeedControlTeacher)
    Stabilization_skill = Skill("Stabilization", StabilizationTeacher)
    selector_skill = Skill("selector", NavigationTeacher) #using the same reward

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)
        Alignment_skill.add_scenario(scenario)
        SpeedControl_skill.add_scenario(scenario)
        Stabilization_skill.add_scenario(scenario)
        selector_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-starship"
            },
            "local": {
               "address": "localhost:1337"
            }
        },
        "env": {
            "name": "starship",
        },
        "training": {},
        "runtime": {
            "workers": 1
        }
    }
    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Navigation_skill)
    agent.add_skill(Alignment_skill)
    #agent.add_skill(SpeedControl_skill)
    #agent.add_skill(Stabilization_skill)
    agent.add_selector_skill(selector_skill, [Navigation_skill, Alignment_skill], fixed_order=True)

    runtime.train(agent, train_iters=1)


if __name__ == "__main__":
    start()
