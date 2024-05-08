import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill, SkillSelector, Trainer
from sensors import sensors
from config import config
from scenarios import Navigation_scenarios
from teacher import (SelectorTeacher, SpeedControlTeacher, StabilizationTeacher,NavigationTeacher)

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

def run_agent():
    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    with SkillSelector("selector", SelectorTeacher) as selector_skill:
        for selector_scenario in Navigation_scenarios:
            selector_skill.add_scenario(Scenario(selector_scenario))

        with Skill("Navigation", NavigationTeacher) as Navigation_skill:
            for scenario_dict in Navigation_scenarios:
                Navigation_skill.add_scenario(Scenario(scenario_dict))
            selector_skill.add_skill(Navigation_skill)

        with Skill("Stabilization", StabilizationTeacher) as Stabilization_skill:
            for scenario_dict in Navigation_scenarios:
                Stabilization_skill.add_scenario(Scenario(scenario_dict))
            selector_skill.add_skill(Stabilization_skill)

        with Skill("SpeedControl", SpeedControlTeacher) as SpeedControl_skill:
            for scenario_dict in Navigation_scenarios:
                SpeedControl_skill.add_scenario(Scenario(scenario_dict))
            selector_skill.add_skill(SpeedControl_skill)

    agent.add_selector_skill(selector_skill, [Navigation_skill, Stabilization_skill, SpeedControl_skill], fixed_order=False, fixed_order_repeat=False)

    # Load a pre-trained agent
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    trainer.train(agent, train_cycles=50)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()
