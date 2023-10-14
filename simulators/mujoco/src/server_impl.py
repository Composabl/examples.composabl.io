#!/usr/bin/env python3
from typing import Any, Dict, SupportsFloat, Tuple

import composabl_core.utils.logger as logger_util
import gymnasium as gym
from composabl_core.agent.scenario import Scenario
from composabl_core.grpc.server.server_composabl import (EnvSpec,
                                                         ServerComposabl)
# Support Envs
from gym_envs.ant import AntEnv
from gym_envs.half_cheetah import HalfCheetahEnv
from gym_envs.hopper import HopperEnv
from gym_envs.humanoid import HumanoidEnv
from gym_envs.humanoidstandup import HumanoidStandupEnv
from gym_envs.inverted_double_pendulum import InvertedDoublePendulumEnv
from gym_envs.inverted_pendulum import InvertedPendulumEnv
from gym_envs.pusher import PusherEnv
from gym_envs.reacher import ReacherEnv
from gym_envs.swimmer import SwimmerEnv
from gym_envs.walker2d import Walker2dEnv

logger = logger_util.get_logger(__name__)

# Implements https://mgoulao.github.io/gym-docs/environments/mujoco/walker2d/
class ServerImpl(ServerComposabl):
    def __init__(self):
        self.env = None
        self.envs_supported = {
            "ant": AntEnv,
            "half_cheetah": HalfCheetahEnv,
            "hopper": HopperEnv,
            "humanoid": HumanoidEnv,
            "humanoidstandup": HumanoidStandupEnv,
            "inverted_double_pendulum": InvertedDoublePendulumEnv,
            "inverted_pendulum": InvertedPendulumEnv,
            "pusher": PusherEnv,
            "reacher": ReacherEnv,
            "swimmer": SwimmerEnv,
            "walker2d": Walker2dEnv,
        }

    def Make(self, env_id: str, env_init: dict) -> EnvSpec:
        env_id = env_id.lower()
        envs_supported_keys = self.envs_supported.keys()

        if env_id not in envs_supported_keys:
            raise Exception("Env ID not supported, supported envs: {}".format(envs_supported_keys))

        # TODO: Check if env_init keys are in the kwargs of the env and then add them
        self.env = self.envs_supported[env_id]()
        return self.env.spec

    def ObservationSpaceInfo(self) -> gym.Space:
        return self.env.observation_space

    def ActionSpaceInfo(self) -> gym.Space:
        return self.env.action_space

    def ActionSpaceSample(self) -> Any:
        return self.env.action_space.sample()

    def Reset(self) -> Tuple[Any, Dict[str, Any]]:
        obs = self.env.reset()
        return obs, {}

    def Step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        obs, reward, done, info = self.env.step(action)
        return obs, reward, done, False, info

    def Close(self):
        if self.env:
            self.env.close()

    def SetScenario(self, scenario):
        self.scenario = scenario

    def GetScenario(self):
        if self.scenario is None:
            return Scenario({"dummy": 0})

        return self.scenario

    def SetRewardFunc(self, reward_func):
        self.env.set_reward_func(reward_func)

    def GetRender(self):
        pass

    def GetRenderMode(self):
        pass

    def SetRenderMode(self, mode):
        pass

