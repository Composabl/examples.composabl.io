import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from config import config
from scenarios import ss1_scenarios, ss2_scenarios, transition_scenarios, selector_scenarios
from teacher import SS1Teacher, SS2Teacher, TransitionTeacher
from composabl import Controller

#from utils.cleanup import cleanup_folder
#from utils.config import generate_config

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

class ProgrammedSelector(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if self.counter >= 0 and self.counter <= 22:
            action = [0]
        elif self.counter >= 76 :
            action = [2]
        else:
            action = [1]

        return action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False



def start():
    #if DELETE_OLD_HISTORY_FILES:
    #    cleanup_folder(PATH_HISTORY)
    #else:
    #    print("|-- Skipping deletion of old history files...")

    ss1_skill = Skill("ss1", SS1Teacher)
    for scenario_dict in ss1_scenarios:
        ss1_skill.add_scenario(Scenario(scenario_dict))

    ss2_skill = Skill("ss2", SS2Teacher)
    for scenario_dict in ss2_scenarios:
        ss2_skill.add_scenario(Scenario(scenario_dict))

    transition_skill = Skill("transition", TransitionTeacher)
    for scenario_dict in transition_scenarios:
        transition_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", ProgrammedSelector)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss2_skill, transition_skill, ss1_skill], fixed_order=False, fixed_order_repeat=False)

    # Load a pre-trained agent
    #cleanup_folder(PATH_CHECKPOINTS, ".DS_Store")

    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_iters=1000)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
