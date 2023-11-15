import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from teacher import MinimizeCostTeacher

license_key = os.environ["COMPOSABL_LICENSE"]


def start():
    machines = Sensor("machines", "")
    repairer_hourly_rate = Sensor("repairer_hourly_rate", "")
    spare_cost = Sensor("spare_cost", "")
    machine_operating_hours = Sensor("machine_operating_hours", "")
    downtime_cost_hourly_machine = Sensor("downtime_cost_hourly_machine", "")
    time_to_failure_min = Sensor("time_to_failure_min", "")
    time_to_failure_max = Sensor("time_to_failure_max", "")
    hours_to_repair_min = Sensor("hours_to_repair_min", "")
    hours_to_repair_max = Sensor("hours_to_repair_max", "")
    cost = Sensor("cost", "")
    spares_level = Sensor("spares_level", "")

    sensors = [machines, repairer_hourly_rate, spare_cost, machine_operating_hours, downtime_cost_hourly_machine, time_to_failure_min, time_to_failure_max, hours_to_repair_min, hours_to_repair_max,
               cost, spares_level]

    Q1_scenarios = [
        {
            "run_time": 8 * 5 * 52  # 1 year
        }
    ]

    MinimizeCost_skill = Skill("MinimizeCost", MinimizeCostTeacher, trainable=True)

    for scenario_dict in Q1_scenarios:
        scenario = Scenario(scenario_dict)
        MinimizeCost_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-maintenance-management"
            }
        },
        "env": {
            "name": "maintenance-management",
        },
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(MinimizeCost_skill)

    runtime.train(agent, train_iters=3)


if __name__ == "__main__":
    start()
