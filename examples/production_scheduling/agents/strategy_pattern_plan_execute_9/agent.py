import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from teacher import BaseTeacher, SelectorTeacher
import datetime

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def start():
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

    # dt=1 minute, we are running for 8hours=480 mins
    high_demand_scenarios = [
        {   # High Demand
            "cookies_demand": [60,100,120],
            "cupcake_demand": [18,30,40],
            "cake_demand": [5,7,10],
        }
    ]

    high_demand_skill = Skill("high_demand", BaseTeacher)
    for scenario_dict in high_demand_scenarios:
        high_demand_skill.add_scenario(Scenario(scenario_dict))

    low_demand_scenarios = [
        {   # Low Demand
            "cookies_demand": [10,20,50],
            "cupcake_demand": [6,10,15],
            "cake_demand": [1,3,4],
        },
    ]

    low_demand_skill = Skill("low_demand", BaseTeacher)
    for scenario_dict in low_demand_scenarios:
        low_demand_skill.add_scenario(Scenario(scenario_dict))


    selector_scenarios = [
        {   
            "cookies_demand": [10,20,30,50,70,80,100],
            "cupcake_demand": [6,10,15,18,20,25,30],
            "cake_demand": [1,3,5,6,7,10,11],
        }
    ]
    selector_skill = Skill("selector", SelectorTeacher)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    config = {
        "license": license_key,
        "target": {
            #"docker": {
            #    "image": "composabl/sim-whisky-local:latest"
            #},
            "local": {
               "address": "localhost:1337"
            }
        },
        "env": {
            "name": "sim-whisky",
        },
        "runtime": {
            "workers": 1,
            "num_gpus": 0
        }
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(high_demand_skill)
    agent.add_skill(low_demand_skill)
    agent.add_selector_skill(selector_skill, [high_demand_skill, low_demand_skill], fixed_order=False, fixed_order_repeat=False)

    
    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    #if len(files) > 0:
    #   agent.load(PATH_CHECKPOINTS)


    runtime.train(agent, train_iters=3)
    
    #agent.export(PATH_CHECKPOINTS)
    end_time = datetime.datetime.now()
    print('Training time: ', end_time - start_time)


if __name__ == "__main__":
    start()

