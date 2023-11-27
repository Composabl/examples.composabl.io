import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from teacher import BalanceTeacher

license_key = os.environ["COMPOSABL_LICENSE"]


def start():
    s0 = Sensor("s0", "rootz (torso) - z-coordinate of the top (height of hopper) (position (m))")
    s1 = Sensor("s1", "rooty (torso) - angle of the top (angle (rad))")
    s2 = Sensor("s2", "thigh_joint - angle of the thigh joint (angle (rad))")
    s3 = Sensor("s3", "leg_joint - angle of the leg joint (angle (rad))")
    s4 = Sensor("s4", "foot_joint - angle of the foot joint (angle (rad))")
    s5 = Sensor("s5", "thigh_left_joint - angle of the left thigh joint (angle (rad))")
    s6 = Sensor("s6", "leg_left_joint - angle of the left leg joint (angle (rad))")
    s7 = Sensor("s7", "foot_left_joint - angle of the left foot joint (angle (rad))")
    s8 = Sensor("s8", "rootx - velocity of the x-coordinate of the top (velocity (m/s))")
    s9 = Sensor("s9", "rootz - velocity of the z-coordinate (height) of the top (velocity (m/s))")
    s10 = Sensor("s10", "rooty - angular velocity of the angle of the top (angular velocity (rad/s))")
    s11 = Sensor("s11", "thigh_joint - angular velocity of the thigh hinge (angular velocity (rad/s))")
    s12 = Sensor("s12", "leg_joint - angular velocity of the leg hinge (angular velocity (rad/s))")
    s13 = Sensor("s13", "foot_joint - angular velocity of the foot hinge (angular velocity (rad/s))")
    s14 = Sensor("s14", "thigh_left_joint - angular velocity of the thigh hinge (angular velocity (rad/s))")
    s15 = Sensor("s15", "leg_left_joint - angular velocity of the leg hinge (angular velocity (rad/s))")
    s16 = Sensor("s16", "foot_left_joint - angular velocity of the foot hinge (angular velocity (rad/s))")

    sensors = [
        s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16
    ]

    balance_scenarios = [
        {
            "s0": 0,
            "s1": 0,
            "s2": 0,
            "s3": 0,
            "s4": 0,
            "s5": 0,
            "s6": 0,
            "s7": 0,
            "s8": 0,
            "s9": 0,
            "s10": 0,
            "s11": 0,
            "s12": 0,
            "s13": 0,
            "s14": 0,
            "s15": 0,
            "s16": 0
        }
    ]

    balance_skill = Skill("Balance", BalanceTeacher, trainable=True)

    for scenario_dict in balance_scenarios:
        scenario = Scenario(scenario_dict)
        balance_skill.add_scenario(scenario)

    config = {
        "license": license_key,
        "target": {
            "local": {
                "address": "localhost:1337"
            }
        },
        "env": {
            "name": "mujoco-walker2d",
        },
        "training": {}
    }
    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(Navigation_skill)

    runtime.train(agent, train_iters=10)


if __name__ == "__main__":
    start()
