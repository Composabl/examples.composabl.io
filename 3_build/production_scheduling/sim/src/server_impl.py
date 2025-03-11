# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Any, Dict, SupportsFloat, Tuple

import gymnasium as gym
from composabl_core.agent.scenario.scenario import Scenario
from composabl_core.networking.server_composabl import ServerComposabl
from sim import ProductionSchedulingEnv


class ServerImpl(ServerComposabl):
    """
    Define the way how Composabl (ServerComposabl) can interact with the simulation environment (SimEnv)
    """
    env: ProductionSchedulingEnv

    def __init__(self, env_init: dict = {}):
        self.env_init = env_init

    async def make(self, env_id: str, env_init: dict):
        self.env_id = env_id if env_id else self.env_id
        self.env_init = env_init if env_init else self.env_init

        print("Creating env_init: ", self.env_init)
        self.env = ProductionSchedulingEnv()

        return {
            "id": "whisky",
            "max_episode_steps": 480
        }

    async def sensor_space_info(self) -> gym.Space:
        return self.env.observation_space

    async def action_space_info(self) -> gym.Space:
        return self.env.action_space

    async def action_space_sample(self) -> Any:
        return self.env.action_space.sample()

    async def reset(self) -> Tuple[Any, Dict[str, Any]]:
        return self.env.reset()

    async def step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        if self.env_id == "case-error":
            raise Exception("Random Error")

        return self.env.step(action)

    async def close(self):
        self.env.close()

    async def set_scenario(self, scenario):
        self.env.scenario = scenario

    async def get_scenario(self):
        if self.env.scenario is None:
            return Scenario({
                "dummy": 0
            })
        return self.env.scenario

    async def set_reward_func(self, reward_func):
        self.env.set_reward_func(reward_func)

    async def set_render_mode(self, render_mode):
        self.env.render_mode = render_mode

    async def get_render_mode(self):
        return self.env.render_mode

    async def get_render(self):
        return self.env.render_frame()
