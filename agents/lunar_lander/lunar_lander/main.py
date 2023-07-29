import os
from composabl.agent import Agent, Scenario, Skill
from composabl_ray import Runtime

from .reward import (
    RewardLand,
    RewardMoveToCenter,
    RewardSelector,
    RewardStabilize,
)

LICENSE_KEY = os.environ.get("LICENSE_KEY", None)


def start():
    stabilize_scenarios = [
        {
            "angle": 0,
            "horizontal_position": [-0.2, 0.2],
            "vertical_position": [-0.5, -0.5],
        },
        {
            "angle": -0.17,
            "horizontal_position": [-0.5, 0.5],
            "vertical_position": [-0.5, -0.25],
            "velocity": 0,
        },
        {
            "angle": 0.12,
            "horizontal_position": [-0.7, 0.7],
            "vertical_position": [-0.65, -0.1],
            "velocity": 0,
        },
    ]

    stabilize_skill = Skill("stabilize", RewardStabilize(), trainable=True)
    for scenario_dict in stabilize_scenarios:
        scenario = Scenario(scenario_dict, reward_threshold=1500)
        stabilize_skill.add_scenario(scenario)

    move_to_center_scenarios = [
        {
            "angle": 0,
            "horizontal_position": [-0.2, 0.2],
            "vertical_position": [-0.5, -0.5],
        },
        {
            "angle": -0.17,
            "horizontal_position": [-0.5, 0.5],
            "vertical_position": [-0.5, -0.25],
            "velocity": 0,
        },
        {
            "angle": 0.12,
            "horizontal_position": [-0.7, 0.7],
            "vertical_position": [-0.65, -0.1],
            "velocity": 0,
        },
    ]

    move_to_center_skill = Skill("move to center", RewardMoveToCenter(), trainable=True)
    for scenario_dict in move_to_center_scenarios:
        scenario = Scenario(scenario_dict, reward_threshold=1500)
        move_to_center_skill.add_scenario(scenario)

    land_scenarios = [
        {
            "angle": 0,
            "horizontal_position": [-0.2, 0.2],
            "vertical_position": [-0.5, -0.5],
        },
        {
            "angle": -0.17,
            "horizontal_position": [-0.5, 0.5],
            "vertical_position": [-0.5, -0.25],
            "velocity": 0,
        },
        {
            "angle": 0.12,
            "horizontal_position": [-0.7, 0.7],
            "vertical_position": [-0.65, -0.1],
            "velocity": 0,
        },
    ]

    land_skill = Skill("land", RewardLand(), trainable=True)
    for scenario_dict in land_scenarios:
        scenario = Scenario(scenario_dict, reward_threshold=150)
        land_skill.add_scenario(scenario)

    selector_skill_scenarios = [
        {
            "angle": 0,
            "horizontal_position": [-0.2, 0.2],
            "vertical_position": [-0.5, -0.5],
        },
        {
            "angle": -0.17,
            "horizontal_position": [-0.5, 0.5],
            "vertical_position": [-0.5, -0.25],
            "velocity": 0,
        },
        {
            "angle": 0.12,
            "horizontal_position": [-0.7, 0.7],
            "vertical_position": [-0.65, -0.1],
            "velocity": 0,
        },
    ]

    selector_skill = Skill("selector", RewardSelector(), trainable=True)
    for scenario_dict in selector_skill_scenarios:
        scenario = Scenario(scenario_dict, reward_threshold=1000)
        selector_skill.add_scenario(scenario)

    config = {
        "env": {
            "name": "lunar_lander_sim",
            "compute": "docker",
            "config": {
                "use_gpu": False,  # @todo: doesn't do anything yet
                "image": "composabl/sim-lunar-lander:latest",
            },
        },
        "license": LICENSE_KEY,
        "training": {},
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)

    agent.add_skill(stabilize_skill)
    agent.add_skill(move_to_center_skill)
    agent.add_skill(land_skill)
    # agent.add_selector_skill(selector_skill, [stabilize_skill, move_to_center_skill, land_skill], fixed_order=True, repeat=False)
    # agent.demo_all_skills(
    #     save_directory="/home/hunter/Videos/lunar_lander/before_training"
    # )
    agent.train(train_iters=500)
    # agent.demo_all_skills(
    #     save_directory="/home/hunter/Videos/lunar_lander/after_training"
    # )
