#!/usr/bin/env python3
from typing import Any, Dict, SupportsFloat, Tuple, Optional

import composabl.utils.logger as logger_util
from composabl.agent.scenario import Scenario
from composabl.grpc.server.server_composabl import ServerComposabl

import gymnasium as gym
from gymnasium.envs.registration import EnvSpec

from .sim import SimEnv

logger = logger_util.get_logger(__name__)


class ServerImpl(ServerComposabl):
    def __init__(self):
        self.env = SimEnv()

    def Make(self, env_id: str) -> EnvSpec:
        spec = {'id': 'my_simulator', 'max_episode_steps': 1000}
        return spec

    def ObservationSpaceInfo(self) -> gym.Space:
        return self.env.observation_space

    def ActionSpaceInfo(self) -> gym.Space:
        return self.env.action_space

    def ActionSpaceSample(self) -> Any:
        return self.env.action_space.sample()

    def Reset(self) -> Tuple[Any, Dict[str, Any]]:
        obs, info = self.env.reset()
        return obs, info

    def Step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        return self.env.step(action)

    def Close(self):
        self.env.close()

    def SetScenario(self, scenario):
        scenario = Scenario.from_proto(scenario)
        self.env.scenario = scenario

    def GetScenario(self):
        if self.env.scenario is None:
            return Scenario({"dummy": 0})

        return self.env.scenario

    def SetRewardFunc(self, reward_func):
        self.env.set_reward_func(reward_func)

    def SetRenderMode(self, render_mode):
        self.env.render_mode = render_mode

    def GetRenderMode(self):
        return self.env.render_mode

    def GetRender(self):
        return self.env.get_render_frame()


