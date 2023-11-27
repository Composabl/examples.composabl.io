import os

from agent.controller import (DecrementController, IncrementController,
                              SelectorController)
from agent.perceptors import perceptors
from agent.scenarios import (decrement_scenarios, increment_scenarios,
                             target_scenarios)
from agent.teacher import DecrementTeacher, IncrementTeacher, SelectorTeacher
from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sim.sim import SimEnv

license_key = os.environ["COMPOSABL_LICENSE"]


def start():
    os.environ["COMPOSABL_EULA_AGREED"] = "1"

    state1 = Sensor("state1", "the counter")
    time_counter = Sensor("time_counter", "the time counter")
    sensors = [state1, time_counter]

    increment_skill_controller = Skill("increment-controller", IncrementController)
    decrement_skill_controller = Skill("decremement-controller", DecrementController)
    increment_skill = Skill("increment", IncrementTeacher)
    for scenario_dict in increment_scenarios:
        scenario = Scenario(scenario_dict)
        increment_skill.add_scenario(scenario)

    decrement_skill = Skill("decremement", DecrementTeacher)
    for scenario_dict in decrement_scenarios:
        scenario = Scenario(scenario_dict)
        decrement_skill.add_scenario(scenario)

    target_skill_controller = Skill("selector-controller", SelectorController)

    target_skill = Skill("selector-teacher", SelectorTeacher)
    for scenario_dict in target_scenarios:
        scenario = Scenario(scenario_dict)
        target_skill.add_scenario(scenario)

    target_skill_sos = Skill("selector-of-selector-teacher", SelectorTeacher)
    for scenario_dict in target_scenarios:
        scenario = Scenario(scenario_dict)
        target_skill_sos.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-demo-discrete:latest"
            }
        },
        "env": {
            "name": "composabl",
            "init": {
                "space_type": "discrete",
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
        [increment_skill_controller, decrement_skill_controller],
        fixed_order=True,
        fixed_order_repeat=False,
    )

    agent.add_selector_skill(
        target_skill,
        [increment_skill, decrement_skill],
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
    agent.train()

if __name__ == "__main__":
    start()
