import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from teacher import ReachTeacher

license_key = os.environ["COMPOSABL_KEY"]


def start():
    # Observation Space
    # The state is an 8-dimensional vector: the coordinates of the lander in `x` & `y`, its linear

    state1 = Sensor("state1", "dummy variable that accumulates an action value")
    time_counter = Sensor("time_counter", "")

    sensors = [state1, time_counter]

    reach_scenarios = [
        {state1: 0, time_counter: 0},
        {state1: -100, time_counter: 0},
        {state1: 100, time_counter: 0},
    ]

    reach_skill = Skill("reach", ReachTeacher, trainable=True)
    for scenario_dict in reach_scenarios:
        scenario = Scenario(scenario_dict)
        reach_skill.add_scenario(scenario)

    config = {
        "target": {
            "kubernetes": {
                # "namespace": "composabl-sims",
                "image": "composabl/sim-cstr:latest",
                "regcred": "composabl-registry",
            }
        },
        "license": license_key,
        "training": {},
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(reach_skill)
    # agent.add_selector_skill(selector_skill, [stabilize_skill, move_to_center_skill, land_skill], fixed_order=True, repeat=False)
    agent.train(train_iters=5)


if __name__ == "__main__":
    start()
