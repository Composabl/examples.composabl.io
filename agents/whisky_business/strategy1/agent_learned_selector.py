import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Controller, SkillGroup
from make_controller import MakeCookieController, MakeCupcakeController, MakeCakeController, MakeWaitController
from sensors import sensors
from teacher import BaseTeacher

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


class ProgrammedSelector(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if obs['order_skill'] == 1: #Make Cookies
            action = [1] #[1,4,7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        elif obs['order_skill'] == 2:
            action = [2] #[2,5,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        elif obs['order_skill'] == 3:
            action = [3] #[3,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        else:
            action = [0]        #Wait by default

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

    selector_scenarios = [
        {
            "order_skill": 0,   #Wait

            "order_skill": 1,   #Make Cookie

            "order_skill": 2,   #Make Cupcake

            "order_skill": 3,   #Make Cake

        }
    ]


    selector_skill = Skill("selector", ProgrammedSelector)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))
    
    make_cookies = Skill("make_cookies", MakeCookieController)
    for scenario_dict in bake_scenarios:
        make_cookies.add_scenario(Scenario(scenario_dict))

    make_cupcakes = Skill("make_cupcakes", MakeCupcakeController)
    for scenario_dict in bake_scenarios:
        make_cupcakes.add_scenario(Scenario(scenario_dict))

    make_cakes = Skill("make_cakes", MakeCakeController)
    for scenario_dict in bake_scenarios:
        make_cakes.add_scenario(Scenario(scenario_dict))

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
            "workers": 1
        }
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(select_product)
    agent.add_skill(make_cookies)
    agent.add_skill(make_cupcakes)
    agent.add_skill(make_cakes)

    agent.add_selector_skill(select_product, [make_cookies, make_cupcakes, make_cakes], fixed_order=False, fixed_order_repeat=True)


    # Initialize the Skill Group
  #  sg = SkillGroup(select_product, make_cookies, make_cupcakes, make_cakes)
  #  agent.add_skill_group(sg)

    files = os.listdir(PATH_CHECKPOINTS)

    if '.DS_Store' in files:
        files.remove('.DS_Store')
        os.remove(PATH_CHECKPOINTS + '/.DS_Store')

    '''try:
        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        os.mkdir(PATH_CHECKPOINTS)'''

    runtime.train(agent, train_iters=2)
    
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()





