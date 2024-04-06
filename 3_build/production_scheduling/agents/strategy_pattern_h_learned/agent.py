import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from teacher import BaseTeacher
from config import config
from scenarios import bake_scenarios
from teacher import CookiesTeacher, CupcakesTeacher, CakesTeacher, WaitTeacher, SelectorTeacher
from perceptors import perceptors

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def run_agent():
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]

        for file in pkl_files:
            file_path = PATH_HISTORY + '/' + file
            os.remove(file_path)
    except:
        pass

    cookies_skill = Skill("cookies", CookiesTeacher)
    cupcakes_skill = Skill("cupcakes", CupcakesTeacher)
    cakes_skill = Skill("cakes", CakesTeacher)
    wait_skill = Skill("wait", WaitTeacher)

    selector_skill = Skill("selector", SelectorTeacher)
    for scenario_dict in bake_scenarios:
        cookies_skill.add_scenario(Scenario(scenario_dict))
        cupcakes_skill.add_scenario(Scenario(scenario_dict))
        cakes_skill.add_scenario(Scenario(scenario_dict))
        wait_skill.add_scenario(Scenario(scenario_dict))

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)
    agent.add_perceptors(perceptors)

    agent.add_skill(cookies_skill)
    agent.add_skill(cupcakes_skill)
    agent.add_skill(cakes_skill)
    agent.add_skill(wait_skill)
    agent.add_selector_skill(selector_skill, [cookies_skill,cupcakes_skill,cakes_skill,wait_skill], fixed_order=False, fixed_order_repeat=False)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    if len(files) > 0:
        agent.load(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=10)

    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    run_agent()

