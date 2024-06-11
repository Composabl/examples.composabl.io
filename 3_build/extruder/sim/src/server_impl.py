# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Any, Dict, SupportsFloat, Tuple

import gymnasium as gym
from composabl_core.agent.scenario.scenario import Scenario
from composabl_core.networking.server_composabl import ServerComposabl
from sim import Env


class ServerImpl(ServerComposabl):
    """
    Define the way how Composabl (ServerComposabl) can interact with the simulation environment (SimEnv)
    """
    env: Env

    def __init__(self, env_init: dict = {}) -> None:
        self.env_init = env_init

    async def make(self, env_id: str, env_init: dict) -> Dict[str, Any]:
        self.env_id = env_id if env_id else self.env_id
        self.env_init = env_init if env_init else self.env_init

        print("Creating env_init: ", self.env_init)
        self.env = Env()

        return {
            "id": "extruder",
            "max_episode_steps": 1000
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

    async def close(self) -> None:
        self.env.close()

    async def set_scenario(self, scenario) -> None:
        self.env.scenario = scenario

    async def get_scenario(self) -> Scenario:
        if self.env.scenario is None:
            return Scenario({
                "dummy": 0
            })
        return self.env.scenario

    async def set_reward_func(self, reward_func) -> None:
        self.env.set_reward_func(reward_func)

    async def set_render_mode(self, render_mode) -> None:
        self.env.render_mode = render_mode

    async def get_render_mode(self) -> None:
        return self.env.render_mode

    async def get_render(self) -> None:
        return self.env.render_frame()
