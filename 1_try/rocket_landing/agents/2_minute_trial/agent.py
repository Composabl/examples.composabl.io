import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Scenario, Skill, Trainer

#from config_k8s import config
from config import config
from scenarios import Navigation_scenarios
from sensors import sensors
from teacher import NavigationTeacher

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

def run_agent():
    Navigation_skill = Skill("Navigation", NavigationTeacher)

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)

    runtime = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Navigation_skill)

    # Load a pre-trained agent
    # try:
    #     if len(os.listdir(PATH_CHECKPOINTS)) > 0:
    #         agent.load(PATH_CHECKPOINTS)
    # except Exception:
    #     print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_cycles=2)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()
