import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from .teacher import (LandTeacher, MoveToCenterTeacher, SelectorTeacher,
                      StabilizeTeacher)

license_key = os.environ["COMPOSABL_KEY"]


def start():
    print("composabl_core|====================================================================")
    print("composabl_core|")
    print("composabl_core|Running the Lunar Lander")

    # Observation Space
    # The state is an 8-dimensional vector: the coordinates of the lander in `x` & `y`, its linear
    # velocities in `x` & `y`, its angle, its angular velocity, and two booleans
    # that represent whether each leg is in contact with the ground or not.

    pos_x = Sensor("position_x", "the position of the lander in the x-axis, normalized (float)")
    pos_y = Sensor("position_y", "the position of the lander in the y-axis, normalized (float)")
    vel_x = Sensor("velocity_x", "the velocity of the lander in the x-axis, normalized (float)")
    vel_y = Sensor("velocity_y", "the velocity of the lander in the y-axis, normalized (float)")
    theta = Sensor("theta", "the angle of the lander (float)")
    alpha = Sensor("alpha", "the angular velocity of the lander (float)")
    leg_1 = Sensor("leg1", "angular velocity of the pole on the cart (Boolean))")
    leg_2 = Sensor("leg2", "angular velocity of the pole on the cart (Boolean))")

    sensors = [pos_x, pos_y, vel_x, vel_y, theta, alpha, leg_1, leg_2]

    stabilize_scenarios = [
        {
            "position_x": 0,
            pos_y: 0,
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.5, 0.5],
            pos_y: [-0.5, -0.25],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: -0.05,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.7, 0.7],
            pos_y: [-0.65, -0.1],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0.1,
            leg_1: 0,
            leg_2: 0,
        },
    ]

    stabilize_skill = Skill("stabilize", StabilizeTeacher, trainable=True)
    for scenario_dict in stabilize_scenarios:
        scenario = Scenario(scenario_dict)
        stabilize_skill.add_scenario(scenario)

    move_to_center_scenarios = [
        {
            pos_x: [-0.2, 0.2],
            pos_y: [-0.5, -0.5],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.5, 0.5],
            pos_y: [-0.5, -0.25],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: -0.17,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.7, 0.7],
            pos_y: [-0.65, -0.1],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0.12,
            leg_1: 0,
            leg_2: 0,
        },
    ]

    move_to_center_skill = Skill("move to center", MoveToCenterTeacher, trainable=True)
    for scenario_dict in move_to_center_scenarios:
        scenario = Scenario(scenario_dict)
        move_to_center_skill.add_scenario(scenario)

    land_scenarios = [
        {
            pos_x: [-0.2, 0.2],
            pos_y: [-0.5, -0.5],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.5, 0.5],
            pos_y: [-0.5, -0.25],
            vel_x: 0,
            vel_y: 0,
            theta: -0.17,
            alpha: 0,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.7, 0.7],
            pos_y: [-0.65, -0.1],
            vel_x: 0,
            vel_y: 0,
            theta: 0.12,
            alpha: 0,
            leg_1: 0,
            leg_2: 0,
        },
    ]

    land_skill = Skill("land", LandTeacher, trainable=True)
    for scenario_dict in land_scenarios:
        scenario = Scenario(scenario_dict)
        land_skill.add_scenario(scenario)

    selector_skill_scenarios = [
        {
            pos_x: [-0.2, 0.2],
            pos_y: [-0.5, -0.5],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.5, 0.5],
            pos_y: [-0.5, -0.25],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: -0.17,
            leg_1: 0,
            leg_2: 0,
        },
        {
            pos_x: [-0.7, 0.7],
            pos_y: [-0.65, -0.1],
            vel_x: 0,
            vel_y: 0,
            theta: 0,
            alpha: 0.12,
            leg_1: 0,
            leg_2: 0,
        },
    ]

    selector_skill = Skill("selector", SelectorTeacher, trainable=True)
    for scenario_dict in selector_skill_scenarios:
        scenario = Scenario(scenario_dict)
        selector_skill.add_scenario(scenario)

    config = {
        "env": {
            "name": "lunar_lander_sim",
            "compute": "local",  # "docker", "kubernetes", "local"
            "config": {
                "address": "localhost:1337",
                # "use_gpu": False,
                # "image": "composabl/sim-lunar-lander:latest"
            },
        },
        "license": license_key,
        "training": {},
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(stabilize_skill)
    agent.add_skill(move_to_center_skill)
    agent.add_skill(land_skill)
    agent.add_selector_skill(selector_skill, [stabilize_skill, move_to_center_skill, land_skill], fixed_order=True, repeat=False)
    agent.train(train_iters=100)
