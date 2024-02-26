import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from teacher import BaseTeacher
from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController, WaitController
from perceptors import perceptors


license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def start():
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]

        for file in pkl_files:
            file_path = PATH_HISTORY + '/' + file
            os.remove(file_path)
    except:
        pass

    # dt=1 minute, we are running for 8hours=480 mins
    high_demand_scenarios = [
        {   # High Demand
            "cookies_demand": 100,
            "cupcake_demand": 18,
            "cake_demand": 5,
        }
    ]

    low_demand_scenarios = [
        {   # Low Demand
            "cookies_demand": 20,
            "cupcake_demand": 6,
            "cake_demand": 1,
        },
    ]
    
    normal_demand_scenarios = [
        {   # Std Demand
            "cookies_demand": 60,
            "cupcake_demand": 18,
            "cake_demand": 2,
        },
    ]

    selector_demand_scenarios = [
        {   # Std Demand
            "cookies_demand": [20,60,100],
            "cupcake_demand": [6,18],
            "cake_demand": [1,2,5],
        },
    ]
    
    high_demand_skill = Skill("high_demand", BaseTeacher)
    for scenario_dict in high_demand_scenarios:
        high_demand_skill.add_scenario(Scenario(scenario_dict))

    low_demand_skill = Skill("low_demand", BaseTeacher)
    for scenario_dict in low_demand_scenarios:
        low_demand_skill.add_scenario(Scenario(scenario_dict))

    normal_demand_skill = Skill("normal_demand", BaseTeacher)
    for scenario_dict in normal_demand_scenarios:
        normal_demand_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", BaseTeacher)
    for scenario_dict in selector_demand_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    config = {
        "license": license_key,
        "target": {
            #"docker": {
            #    "image": "composabl/sim-cstr:latest"
            #},
            "local": {
               "address": "localhost:1337"
            }
        },
        "env": {
            "name": "sim-whisky",
        },
        "runtime": {
            "workers": 1
        }
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(high_demand_skill)
    agent.add_skill(low_demand_skill)
    agent.add_skill(normal_demand_skill)
    agent.add_selector_skill(selector_skill, [high_demand_skill, normal_demand_skill, low_demand_skill], fixed_order=False, fixed_order_repeat=False)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    try:
        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=30)
    
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()

