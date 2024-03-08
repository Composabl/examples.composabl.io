import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from teacher import BaseTeacher
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
    bake_scenarios = [
        {   # High Demand
            "cookies_demand": 100,
            "cupcake_demand": 18,
            "cake_demand": 5,
        },
        {   # Std Demand
            "cookies_demand": 60,
            "cupcake_demand": 18,
            "cake_demand": 2,
        },
        {   # Low Demand
            "cookies_demand": 20,
            "cupcake_demand": 6,
            "cake_demand": 1,
        },
        {   # Xmas Demand
            "cookies_demand": 260,
            "cupcake_demand": 10,
            "cake_demand": 1,
        },
        {   # Cupcake Wars
            "cookies_demand": 0,
            "cupcake_demand": 96,
            "cake_demand": 0,
        },
        {   # Cookie Wars
            "cookies_demand": 396,
            "cupcake_demand": 0,
            "cake_demand": 0,
        },
        {   # November Birthday
            "cookies_demand": 0,
            "cupcake_demand": 0,
            "cake_demand": 11,
        }
    ]

    produce_skill = Skill("produce", BaseTeacher)
    for scenario_dict in bake_scenarios:
        produce_skill.add_scenario(Scenario(scenario_dict))

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

    agent.add_skill(produce_skill)
    
    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    #if len(files) > 0:
    #   agent.load(PATH_CHECKPOINTS)


    runtime.train(agent, train_iters=2)
    
    agent.export(PATH_CHECKPOINTS)
    end_time = datetime.datetime.now()
    print('Training time: ', end_time - start_time)


if __name__ == "__main__":
    start()

