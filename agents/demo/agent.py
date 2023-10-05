import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from .controller import (DecrementController, IncrementController, SelectorController)
from .perceptors import perceptors
from .scenarios import (decrement_scenarios, increment_scenarios, target_scenarios)
from .sim import SimEnv
from .teacher import DecrementTeacher, IncrementTeacher, SelectorTeacher

license_key = os.environ["COMPOSABL_KEY"]


def start():
    os.environ["COMPOSABL_EULA_AGREED"] = "1"

    state1 = Sensor("state1", "the counter")
    time_counter = Sensor("time_counter", "the time counter")
    sensors = [state1, time_counter]

    increment_skill_controller = Skill("increment-controller", IncrementController, trainable=False)
    decrement_skill_controller = Skill("decremement-controller", DecrementController, trainable=False)

    increment_skill = Skill("increment", IncrementTeacher, trainable=True)
    for scenario_dict in increment_scenarios:
        scenario = Scenario(scenario_dict)
        increment_skill.add_scenario(scenario)

    decrement_skill = Skill("decremement", DecrementTeacher, trainable=True)
    for scenario_dict in decrement_scenarios:
        scenario = Scenario(scenario_dict)
        decrement_skill.add_scenario(scenario)

    target_skill_controller = Skill("selector-controller", SelectorController, trainable=False)

    target_skill = Skill("selector-teacher", SelectorTeacher, trainable=True)
    for scenario_dict in target_scenarios:
        scenario = Scenario(scenario_dict)
        target_skill.add_scenario(scenario)

    target_skill_sos = Skill("selector-of-selector-teacher", SelectorTeacher, trainable=True)
    for scenario_dict in target_scenarios:
        scenario = Scenario(scenario_dict)
        target_skill_sos.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            # One of the below
            "kubernetes": {
                "image": "composabl/sim-demo:latest",
                # "regcred": "composabl-registry",
                # "namespace": "composabl-sims",
            },
            # "docker": {
            #     "image": "composabl/sim-cstr:latest",
            #     # "registry": {
            #     #     "username": "composabl",
            #     #     "password": "composabl",
            #     #     "url": "https://index.docker.io/v1/",
            #     # }
            # },
            # "local": {
            #     "address": "localhost:1337"
            # }
        },
        "env": {
            "name": "composabl",
            "init": {
                "hello": "world"
            }
        },
        "runtime": {
            "ray": {
                # "address": "ray://127.0.0.1:10001",
                "workers": 1
            }
        },
    }

    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)
    agent.add_perceptors(perceptors)

    agent.add_skill(increment_skill)
    agent.add_skill(decrement_skill)
    agent.add_skill(increment_skill_controller)
    agent.add_skill(decrement_skill_controller)
    agent.add_selector_skill(
        target_skill_controller,
        [increment_skill, decrement_skill_controller],
        fixed_order=True,
        fixed_order_repeat=False,
    )

    agent.add_selector_skill(
        target_skill,
        [increment_skill_controller, decrement_skill],
        fixed_order=True,
        fixed_order_repeat=False,
    )

    agent.add_selector_skill(
        target_skill_sos,
        [target_skill, target_skill_controller],
        fixed_order=False,
        fixed_order_repeat=False,
    )

    # let's train the agent!
    agent.train(train_iters=1)

    # Export the agent to the specified directory then re-load it and resume training
    directory = os.path.join(os.getcwd(), "model")
    agent.export(directory)
    agent.load(directory)

    agent.train(train_iters=5)

    # Create a callable agent that can be used to execute the agent skill heirarchy
    trained_agent = agent.prepare()

    # Run the trained_agent on the sim
    sim = SimEnv()
    for _episode_idx in range(5):
        print(f"episode {_episode_idx}")
        obs, _info = sim.reset()
        for _step_index in range(100):
            action = trained_agent.execute(obs)
            obs, _reward, done, _truncated, _info = sim.step(action)

if __name__ == "__main__":
    start()
