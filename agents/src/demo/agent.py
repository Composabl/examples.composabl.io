from composabl import Agent, Runtime, Scenario, Sensor, Skill

from .teacher import ReachTeacher


def start():
    print("composabl_core|====================================================================")
    print("composabl_core|")
    print("composabl_core|Running the Demo Agent")

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
        "env": {
            "name": "sim-demo",
            "compute": "local",  # "docker", "kubernetes", "local"
            "config": {
                "address": "localhost:1337",
                # "use_gpu": False,  # @todo: doesn't do anything yet
                # "image": "composabl/sim-lunar-lander:latest"
            },
        },
        "license": "FPWZ0N-AA478X-7KBZW4-SBRUZ2-S9203L",
        "training": {},
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(reach_skill)
    # agent.add_selector_skill(selector_skill, [stabilize_skill, move_to_center_skill, land_skill], fixed_order=True, repeat=False)
    agent.train(train_iters=5)
