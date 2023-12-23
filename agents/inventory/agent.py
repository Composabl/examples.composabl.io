import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import BalanceTeacher

license_key = os.environ["COMPOSABL_KEY"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

def start():
    Q1_scenarios = [
        {
            "holding_cost": 2,
            "cost_price": 20,
            "delay_days_until_delivery": 5,
            "customer_demand_min": 1,
            "customer_demand_max": 3,
            "selling_price": 25,
            "run_time": 30
        }
    ]

    Balance_skill = Skill("Balance", BalanceTeacher, trainable=True)

    for scenario_dict in Q1_scenarios:
        scenario = Scenario(scenario_dict)
        Balance_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            #"docker": {
            #    "image": "composabl/sim-inventory-management"
            #},
            "local": {
                "address": "localhost:1337"
            }

        },
        "env": {
            "name": "inventory-management",
        },
        "training": {}
    }

    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(Balance_skill)

    files = os.listdir(PATH_CHECKPOINTS)
    if '.DS_Store' in files:
        files.remove('.DS_Store')

    if len(files) > 0:
        #load agent
        agent.load(PATH_CHECKPOINTS)


    agent.train(train_iters=3)

    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
