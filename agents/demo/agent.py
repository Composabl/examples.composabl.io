import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from controller import DecrementController, IncrementController, SelectorController
from perceptors import perceptors
from scenarios import decrement_scenarios, increment_scenarios, target_scenarios
from sim import SimEnv
from teacher import DecrementTeacher, IncrementTeacher, SelectorTeacher

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
        "env": {
            "init": {
                "test": "test"
            },
            "name": "sim-demo",
            "compute": "docker",  # "docker", "kubernetes", "local"
            "config": {
                "image": "composabl/sim-demo:latest",
            }
        },
        "license": "GWLZ5B-JB4X03-KB65G6-XGK84T-OZAPVZ",
        "training": {},
        "flags": {"print_debug_info": True},
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

    directory = "/home/hunter/Documents/checkpoint_test"
    agent.train(train_iters=3)
    agent.export(directory)
    import pickle
    with open("/home/hunter/Documents/checkpoint_test/increment/algorithm_state.pkl", "rb") as f:
        data = pickle.load(f)
        print(data, "=====================")

    agent.load(directory)
    agent.train(train_iters=5)

    trained_agent = agent.prepare()

    sim = SimEnv()
    for _episode_idx in range(5):
        print(f"episode {_episode_idx}")
        obs, _info = sim.reset()
        for _step_index in range(100):
            action = trained_agent.execute(obs)
            obs, _reward, done, _truncated, _info = sim.step(action)

if __name__ == "__main__":
    start()