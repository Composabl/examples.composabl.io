import os

from composabl import Agent, Scenario, Skill, Trainer
from sensors import sensors
from teacher import NavigationTeacher

license_key = os.environ["COMPOSABL_LICENSE"]

def start():

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

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            # "docker": {
            #     "image": "composabl/sim-starship-local"
            # },
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
    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Navigation_skill)

    # Start training the agent
    trainer.train(agent, train_cycles=20)


if __name__ == "__main__":
    start()
