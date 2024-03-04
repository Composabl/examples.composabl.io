import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller
from sensors import sensors
from teacher import BaseTeacher, CookiesTeacher, CupcakesTeacher, CakesTeacher, WaitTeacher
from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController, WaitController


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

    #cookies_skill = Skill("cookies", MakeCookieController)
    #cupcakes_skill = Skill("cupcakes", MakeCupcakeController)
    #cakes_skill = Skill("cakes", MakeCakeController)
    #wait_skill = Skill("wait", WaitController)
    cookies_skill = Skill("cookies", CookiesTeacher)
    cupcakes_skill = Skill("cupcakes", CupcakesTeacher)
    cakes_skill = Skill("cakes", CakesTeacher)
    wait_skill = Skill("wait", WaitTeacher)

    selector_skill = Skill("selector", BaseTeacher)
    for scenario_dict in bake_scenarios:
        cookies_skill.add_scenario(Scenario(scenario_dict))
        cupcakes_skill.add_scenario(Scenario(scenario_dict))
        cakes_skill.add_scenario(Scenario(scenario_dict))
        wait_skill.add_scenario(Scenario(scenario_dict))

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

    agent.add_skill(cookies_skill)
    agent.add_skill(cupcakes_skill)
    agent.add_skill(cakes_skill)
    agent.add_skill(wait_skill)
    agent.add_selector_skill(selector_skill, [cookies_skill,cupcakes_skill,cakes_skill,wait_skill], fixed_order=False, fixed_order_repeat=False)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    try:
        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=10)
    
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()

