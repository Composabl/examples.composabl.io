import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from teacher import TemperatureControlTeacher

license_key = os.environ["COMPOSABL_LICENSE"]


def start():
    y1 = Sensor("y1", "Temperature")
    y1ref = Sensor("y1ref", "")
    u1 = Sensor("u1", "")
    rms = Sensor("rms", "")

    sensors = [y1, y1ref, u1, rms]

    TemperatureControl_scenarios = [
        {
            "y1_SP": 170,
            "time_delay": 0.028
        }
    ]

    TemperatureControl_skill = Skill("TemperatureControl", TemperatureControlTeacher, trainable=True)

    for scenario_dict in TemperatureControl_scenarios:
        scenario = Scenario(scenario_dict)
        TemperatureControl_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-filament-extruder"
            }
        },
        "env": {
            "name": "airplane",
        },
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(TemperatureControl_skill)

    runtime.train(agent, train_iters=3)


if __name__ == "__main__":
    start()
