# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import simpy as sp
from composabl_core.agent.scenario import Scenario


class Env(gym.Env):
    def __init__(self):
        """
        actions = 2 :
            repairers_capacity: repaires capacity allocated for this process
            spares_capacity: spares capacity allocated for this process
        sensor_variables = 11 :
            "machines": Number of equal machines in operation
            "repairer_hourly_rate ": hourly ratefor repairers
            "spare_cost": cost of each spare
            "machine_operating_hours": machine operating hours
            "downtime_cost_hourly_machine": downtime hourly cost per machine
            "time_to_failure_min": minimum time to failure
            "time_to_failure_max": maximum time to failure
            "hours_to_repair_min": minimum hours to repair
            "hours_to_repair_max": maximum hours to repair
            "cost": total cost
            "spares_level": spares level
        run_time: time in hours to run the simulation (simpy)
        """
        obs_space = {
            "machines": {"low": 0, "high": 1e10},
            "repairer_hourly_rate ": {"low": 0, "high": 1e10},
            "spare_cost": {"low": 0, "high": 1e10},
            "machine_operating_hours": {"low": 0, "high": 1e10},
            "downtime_cost_hourly_machine": {"low": 0, "high": 1e10},
            "time_to_failure_min": {"low": 0, "high": 1e10},
            "time_to_failure_max": {"low": 0, "high": 1e10},
            "hours_to_repair_min": {"low": 0, "high": 1e10},
            "hours_to_repair_max": {"low": 0, "high": 1e10},
            "cost": {"low": 0, "high": 1e10},
            "spares_level": {"low": 0, "high": 1e10},
        }

        low_list = [x["low"] for x in obs_space.values()]
        high_list = [x["high"] for x in obs_space.values()]

        self.sensor_space = gym.spaces.Box(
            low=np.array(low_list), high=np.array(high_list)
        )

        action_space = {
            "repairers_capacity": {"low": 1, "high": 100},  # 3
            "spares_capacity": {"low": 1, "high": 1e3},  # 20
        }

        low_act_list = [x["low"] for x in action_space.values()]
        high_act_list = [x["high"] for x in action_space.values()]

        self.action_space = gym.spaces.Box(
            low=np.array(low_act_list), high=np.array(high_act_list)
        )

        self.scenario: Scenario = None

        self.machines = 50
        self.repairer_hourly_rate = 3.75
        self.spare_cost = 30
        self.machine_operating_hours = 8
        self.downtime_cost_hourly_machine = 20
        self.time_to_failure_min = 132
        self.time_to_failure_max = 182
        self.hours_to_repair_min = 4
        self.hours_to_repair_max = 10

        self.run_time = 8 * 5 * 52  # 1 year

        self.obs_time = []
        self.obs_cost = []
        self.obs_spares = []

    def operate_machine(
        self,
        env,
        repairers,
        spares,
        downtime_cost_hourly_machine,
        time_to_failure_min,
        time_to_failure_max,
        hours_to_repair_min,
        hours_to_repair_max,
    ):
        global cost

        while True:
            yield env.timeout(
                self.time_to_failure(time_to_failure_min, time_to_failure_max)
            )
            t_broken = env.now
            # print(f'{env.now} machine broke')
            env.process(
                self.repair_machine(
                    env, repairers, spares, hours_to_repair_min, hours_to_repair_max
                )
            )
            yield spares.get(1)  # wait for 1 spare
            t_replaced = env.now
            # print(f'{env.now} machine replaced')
            cost += downtime_cost_hourly_machine * (t_replaced - t_broken)

    def repair_machine(
        self, env, repairers, spares, hours_to_repair_min, hours_to_repair_max
    ):
        with repairers.request() as request:
            yield request
            yield env.timeout(
                self.generate_repair_time(hours_to_repair_min, hours_to_repair_max)
            )
            yield spares.put(1)
        # print(f"{env.now} repair complete")

    def time_to_failure(self, time_to_failure_min, time_to_failure_max):
        return np.random.uniform(time_to_failure_min, time_to_failure_max)

    def generate_repair_time(self, hours_to_repair_min, hours_to_repair_max):
        return np.random.uniform(hours_to_repair_min, hours_to_repair_max)

    def factory_run(
        self,
        env,
        repairers,
        spares,
        machines=50,
        repairer_hourly_rate=3.75,
        spare_cost=30,
        machine_operating_hours=8,
        downtime_cost_hourly_machine=20,
        time_to_failure_min=132,
        time_to_failure_max=182,
        hours_to_repair_min=4,
        hours_to_repair_max=10,
    ):

        global cost

        cost = 0

        for i in range(machines):
            env.process(
                self.operate_machine(
                    env,
                    repairers,
                    spares,
                    downtime_cost_hourly_machine,
                    time_to_failure_min,
                    time_to_failure_max,
                    hours_to_repair_min,
                    hours_to_repair_max,
                )
            )

        while True:
            cost += (
                repairer_hourly_rate * machine_operating_hours * repairers.capacity
                + spare_cost * spares.capacity
            )
            yield env.timeout(machine_operating_hours)

    def observe_values(self, env, spares):
        global cost

        while True:
            self.obs_time.append(env.now)
            self.obs_cost.append(cost)
            self.obs_spares.append(spares.level)
            obs_dt = 0.1
            yield env.timeout(obs_dt)  # hour

    def reset(self):
        # Define scenario in the simulation
        if isinstance(self.scenario, Scenario):
            sample = self.scenario.sample()

            for key in list(sample.keys()):
                setattr(self, key, sample[key])
        else:
            self.machines = 50
            self.repairer_hourly_rate = 3.75
            self.spare_cost = 30
            self.machine_operating_hours = 8
            self.downtime_cost_hourly_machine = 20
            self.time_to_failure_min = 132
            self.time_to_failure_max = 182
            self.hours_to_repair_min = 4
            self.hours_to_repair_max = 10
            self.run_time = 30

        # time counter
        self.cnt = 0

        self.obs = {
            "machines": self.machines,
            "repairer_hourly_rate ": self.repairer_hourly_rate,
            "spare_cost": self.spare_cost,
            "machine_operating_hours": self.machine_operating_hours,
            "downtime_cost_hourly_machine": self.downtime_cost_hourly_machine,
            "time_to_failure_min": self.time_to_failure_min,
            "time_to_failure_max": self.time_to_failure_max,
            "hours_to_repair_min": self.hours_to_repair_min,
            "hours_to_repair_max": self.hours_to_repair_max,
            "cost": 0,
            "spares_level": 0,
        }

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, info

    def set_scenario(self, scenario):
        self.scenario = scenario

    def step(self, action):
        repairers_capacity = action[0]
        spares_capacity = action[1]

        simpyenv = sp.Environment()

        repairers = sp.Resource(simpyenv, capacity=repairers_capacity)
        spares = sp.Container(simpyenv, init=spares_capacity, capacity=spares_capacity)

        simpyenv.process(
            self.factory_run(
                simpyenv,
                repairers,
                spares,
                machines=self.machines,
                repairer_hourly_rate=self.repairer_hourly_rate,
                spare_cost=self.spare_cost,
                machine_operating_hours=self.machine_operating_hours,
                downtime_cost_hourly_machine=self.downtime_cost_hourly_machine,
                time_to_failure_min=self.time_to_failure_min,
                time_to_failure_max=self.time_to_failure_max,
                hours_to_repair_min=self.hours_to_repair_min,
                hours_to_repair_max=self.hours_to_repair_max,
            )
        )

        simpyenv.process(self.observe_values(simpyenv, spares))

        simpyenv.run(until=self.run_time)  # days

        # TODO: new features
        # order max, order mean, balance total, balance mean, balance min,
        # inventory max, inventory min, inventory mean, inventory std
        # times ordered

        # Increase time counter
        self.cnt += 1

        # REWARD
        reward = 0

        done = False

        # Constraints to break the simulation
        if self.cnt == self.run_time:
            done = True

        self.obs = {
            "machines": self.machines,
            "repairer_hourly_rate ": self.repairer_hourly_rate,
            "spare_cost": self.spare_cost,
            "machine_operating_hours": self.machine_operating_hours,
            "downtime_cost_hourly_machine": self.downtime_cost_hourly_machine,
            "time_to_failure_min": self.time_to_failure_min,
            "time_to_failure_max": self.time_to_failure_max,
            "hours_to_repair_min": self.hours_to_repair_min,
            "hours_to_repair_max": self.hours_to_repair_max,
            "cost": self.obs_cost[-1],
            "spares_level": self.obs_spares[-1],
        }

        self.obs = np.array(list(self.obs.values()))
        info = {}
        return self.obs, reward, done, False, info

    def render(self, mode="human", close=False):
        plt.plot(self.obs_time, self.obs_spares)
        plt.xlabel("Simulation time (hours)")
        plt.ylabel("Spares level")
        plt.show()

        plt.plot(self.obs_time, self.obs_cost)
        plt.xlabel("Simulation time (hours")
        plt.ylabel("Cost History ($)")
        plt.show()
