import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Trainer, Scenario, Skill, SkillGroup
from composabl_core.agent.skill.skill_options import SkillOptions
from sensors import sensors
from config import config
from scenarios import TemperatureControl_scenarios
from gymnasium import spaces

from controller import PIDController
from teacher import DRLTeacher

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/model"

def run_agent():
    PID_control_skill = Skill("PIDControl", PIDController)

    for scenario_dict in TemperatureControl_scenarios:
        scenario = Scenario(scenario_dict)
        PID_control_skill.add_scenario(scenario)


    control_skill = Skill("control", DRLTeacher, SkillOptions(
        action_space=spaces.Box(low=0, high=400, shape=(1,))
    ))

    for scenario_dict in TemperatureControl_scenarios:
        control_skill.add_scenario(Scenario(scenario_dict))

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(control_skill)
    skill_group = SkillGroup(control_skill, PID_control_skill)
    agent.add_skill_group(skill_group)

    #agent.load(PATH_CHECKPOINTS)

    trainer.train(agent, train_cycles=100)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS, dir_exist_ok = True)


if __name__ == "__main__":
    run_agent()
