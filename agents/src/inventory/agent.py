import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill

from .teacher import BalanceTeacher

license_key = os.environ["COMPOSABL_KEY"]


def start():
    print("composabl_core|====================================================================")
    print("composabl_core|")
    print("composabl_core|Running the Inventory Agent")

    inventory_sensor = Sensor("inventory", "")
    balance_sensor = Sensor("balance", "")
    num_ordered_sensor = Sensor("num_ordered", "")
    holding_cost = Sensor("holding_cost", "")
    cost_price = Sensor("cost_price", "")
    delay_days_until_delivery = Sensor("delay_days_until_delivery", "")
    customer_demand_min = Sensor("customer_demand_min", "")
    customer_demand_max = Sensor("customer_demand_max", "")
    selling_price = Sensor("selling_price", "")

    sensors = [inventory_sensor, balance_sensor, num_ordered_sensor, holding_cost, cost_price, delay_days_until_delivery, customer_demand_min, customer_demand_max, selling_price]

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

    Balance_skill = Skill("Balance", BalanceTeacher, trainable=True)

    for scenario_dict in Q1_scenarios:
        scenario = Scenario(scenario_dict)
        Balance_skill.add_scenario(scenario)

    config = {
        "env": {
            "name": "inventory_management",
            "compute": "local",  # "docker", "kubernetes", "local"
            "strategy": "local",  # "docker", "kubernetes", "local"
            "config": {
                "address": "localhost:1337",
                # "image": "composabl.ai/sim-gymnasium:latest"
            }
        },
        "license": license_key,
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(Balance_skill)

    agent.train(train_iters=3)
