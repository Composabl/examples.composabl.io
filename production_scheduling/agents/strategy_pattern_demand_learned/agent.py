import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from config import config
from scenarios import high_demand_scenarios, low_demand_scenarios, normal_demand_scenarios, selector_demand_scenarios
from teacher import BaseTeacher, SelectorTeacher
from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController, WaitController
from perceptors import perceptors
import datetime

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def run_agent():
    start_time = datetime.datetime.now()
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]

        for file in pkl_files:
            file_path = PATH_HISTORY + '/' + file
            os.remove(file_path)
    except:
        pass

    high_demand_skill = Skill("high_demand", BaseTeacher)
    for scenario_dict in high_demand_scenarios:
        high_demand_skill.add_scenario(Scenario(scenario_dict))

    low_demand_skill = Skill("low_demand", BaseTeacher)
    for scenario_dict in low_demand_scenarios:
        low_demand_skill.add_scenario(Scenario(scenario_dict))

    normal_demand_skill = Skill("normal_demand", BaseTeacher)
    for scenario_dict in normal_demand_scenarios:
        normal_demand_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", SelectorTeacher)
    for scenario_dict in selector_demand_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)
    agent.add_perceptors(perceptors)

    agent.add_skill(high_demand_skill)
    agent.add_skill(low_demand_skill)
    agent.add_skill(normal_demand_skill)
    agent.add_selector_skill(selector_skill, [high_demand_skill, normal_demand_skill, low_demand_skill], fixed_order=False, fixed_order_repeat=False)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    if len(files) > 0:
        agent.load(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=3)

    agent.export(PATH_CHECKPOINTS)
    end_time = datetime.datetime.now()
    print('Time to train: ', end_time - start_time)


if __name__ == "__main__":
    run_agent()

