import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import BalanceTeacher

license_key = os.environ["COMPOSABL_LICENSE"]

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
            "run_time": 60
        }
    ]

    Balance_skill = Skill("Balance", BalanceTeacher)

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
        "runtime": {
            "workers": 1
        }
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Balance_skill)

    files = os.listdir(PATH_CHECKPOINTS)

    try:
        files = os.listdir(PATH_CHECKPOINTS)

        if '.DS_Store' in files:
            files.remove('.DS_Store')
            os.remove(PATH_CHECKPOINTS + '/.DS_Store')

        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)

    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    runtime.train(agent, train_iters=10)
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
