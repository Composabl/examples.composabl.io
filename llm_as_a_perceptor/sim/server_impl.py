# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Any, Dict, SupportsFloat, Tuple

import gymnasium as gym

from composabl_core.agent.scenario.scenario import Scenario
from sim import Sim
from composabl_core.networking.server_composabl import ServerComposabl


class ServerImpl(ServerComposabl):
    """
    Define the way how Composabl (ServerComposabl) can interact with the simulation environment (SimEnv)
    """
    def __init__(self, *args, **kwargs):
        self.env_init = kwargs.get("env_init", {})

    async def make(self, env_id: str, env_init: dict):
        self.env_id = env_id if env_id else self.env_id
        self.env_init = env_init if env_init else self.env_init

        print("Creating with env_init: ", self.env_init)
        self.env = Sim(self.env_init)

        return {
            "id": "my_simulator",
            "max_episode_steps": 1000
        }

    async def sensor_space_info(self) -> gym.Space:
        return self.env.sensor_space

    async def action_space_info(self) -> gym.Space:
        return self.env.action_space

    async def action_space_sample(self) -> Any:
        return self.env.action_space.sample()

    async def reset(self) -> Tuple[Any, Dict[str, Any]]:
        return self.env.reset()

    async def step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
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

    async def get_render(self):
        return self.env.render_frame()
