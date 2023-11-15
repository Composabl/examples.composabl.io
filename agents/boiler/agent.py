import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from teacher import LevelTeacher, PressureTeacher, TemperatureTeacher

license_key = os.environ["COMPOSABL_LICENSE"]


def start():
    y1 = Sensor("y1", "drum level")
    y2 = Sensor("y2", "drum pressure")
    y3 = Sensor("y3", "drum temperature")
    y1ref = Sensor("y1ref", "")
    y2ref = Sensor("y2ref", "")
    y3ref = Sensor("y3ref", "")
    u1 = Sensor("u1", "feed water flow rate")
    u2 = Sensor("u2", "fuel flow rate")
    u3 = Sensor("u3", "spray flow rate")

    sensors = [y1, y2, y3, y1ref, y2ref, y3ref, u1, u2, u3]

    y1_scenarios = [
        {
            "signal": "y1",
            "eff_nox_red": 0.7
        }
    ]

    Level_skill = Skill("Level", LevelTeacher, trainable=True)

    for scenario_dict in y1_scenarios:
        scenario = Scenario(scenario_dict)
        Level_skill.add_scenario(scenario)

    y2_scenarios = [
        {
            "signal": "y2",
            "eff_nox_red": 0.7
        }
    ]

    Pressure_skill = Skill("Pressure", PressureTeacher, trainable=True)

    for scenario_dict in y2_scenarios:
        scenario = Scenario(scenario_dict)
        Pressure_skill.add_scenario(scenario)

    y3_scenarios = [
        {
            "signal": "y3",
            "eff_nox_red": 0.7
        }
    ]

    Temperature_skill = Skill("Temperature", TemperatureTeacher, trainable=True)

    for scenario_dict in y3_scenarios:
        scenario = Scenario(scenario_dict)
        Temperature_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-industrial-boiler"
            }
        },
        "env": {
            "name": "industrial-boiler",
        },
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Level_skill)
    agent.add_skill(Pressure_skill)
    agent.add_skill(Temperature_skill)

    runtime.train(agent, train_iters=3)


if __name__ == "__main__":
    start()
