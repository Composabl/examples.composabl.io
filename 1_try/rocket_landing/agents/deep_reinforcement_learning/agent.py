import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Trainer, Scenario, Skill
from teacher import NavigationTeacher, GoalTeacher, LandTeacher
from sensors import sensors
#from config_k8s import config
from config import config
from scenarios import Navigation_scenarios

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/model"

def run_agent():
    Navigation_skill = Skill("Navigation", LandTeacher)

    for scenario_dict in Navigation_scenarios:
        scenario = Scenario(scenario_dict)
        Navigation_skill.add_scenario(scenario)

    trainer = Trainer(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Navigation_skill)

    # Load a pre-trained agent
    #try:
    #    if len(os.listdir(PATH_CHECKPOINTS)) > 0:
    #        agent.load(PATH_CHECKPOINTS)
    #except Exception:
    #    print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    trainer.train(agent, train_cycles=5)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS, dir_exist_ok = True)


if __name__ == "__main__":
    run_agent()
