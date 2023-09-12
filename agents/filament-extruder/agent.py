import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from teacher import TemperatureControlTeacher

license_key = os.environ["COMPOSABL_KEY"]


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
        "env": {
            "name": "filament_extruder",
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

    agent.add_skill(TemperatureControl_skill)

    agent.train(train_iters=3)


if __name__ == "__main__":
    start()
