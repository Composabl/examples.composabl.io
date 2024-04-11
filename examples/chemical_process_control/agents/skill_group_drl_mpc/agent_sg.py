from asyncore import loop
import os
import sys
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from composabl import Agent, Runtime, Scenario, Skill, SkillController, SkillGroup
from sensors import sensors
from config import config
from scenarios import reaction_scenarios
from teacher import CSTRMPCTeacher
from mpc_model import mpc
import numpy as np

PATH: str = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY: str = f"{PATH}/history"
PATH_CHECKPOINTS : str = f"{PATH}/checkpoints"

DELETE_OLD_HISTORY_FILES: bool = True

# Define your skill controller
class MPCControl(SkillController):
    """
    The strategy of this controller is to almost always take the correct action. X% of the time
    it will still take a counter action (hallucination)
    """
    def __init__(self):
        self.count = 0

    async def compute_action(self, obs):
        MPC_Tc = mpc(0, obs['Cref'], obs['Ca'], obs['T'], obs['Tc'])

        dTc_MPC = MPC_Tc[0][0] - obs['Tc']
        dTc_MPC = np.clip(dTc_MPC,-10,10)
        action = dTc_MPC

        action = [MPC_Tc]

        return action

    async def transform_obs(self, obs):
        return obs

    async def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    async def compute_success_criteria(self, transformed_obs, action):
        return False

    async def compute_termination(self, transformed_obs, action):
        return False


async def run_agent():
    """Starting the agent."""

    control_skill = Skill("control", CSTRMPCTeacher)
    for scenario_dict in reaction_scenarios:
        control_skill.add_scenario(Scenario(scenario_dict))

    # Define it as a Skill
    mpc_control = Skill("mpc_controller", MPCControl)

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(control_skill)
    agent.add_skill(mpc_control)

    # Initialize the Skill Group
    sg = SkillGroup(control_skill, mpc_control)
    agent.add_skill_group(sg)

    # Load a pre-trained agent
    try:
        if len(os.listdir(PATH_CHECKPOINTS)) > 0:
            agent.load(PATH_CHECKPOINTS)
    except Exception:
        print("|-- No checkpoints found. Training from scratch...")

    # Start training the agent
    runtime.train(agent, train_iters=2)

    # Save the trained agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_agent())
