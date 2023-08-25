from typing import Any, Dict, SupportsFloat, Tuple

import composabl_core.utils.logger as logger_util
import gymnasium as gym
from composabl_core.agent.scenario import Scenario
from composabl_core.grpc.server.server_composabl import ServerComposabl
from gymnasium.envs.registration import EnvSpec

from sim import SimEnv

logger = logger_util.get_logger(__name__)


class ServerImpl(ServerComposabl):
    """
    Define the way how Composabl (ServerComposabl) can interact with the simulation environment (SimEnv)
    """
    def __init__(self):
        self.env = SimEnv()

    def Make(self, env_id: str) -> EnvSpec:
        return {
            "id": "my_simulator",
            "max_episode_steps": 1000
        }

    def ObservationSpaceInfo(self) -> gym.Space:
        return self.env.observation_space

    def ActionSpaceInfo(self) -> gym.Space:
        return self.env.action_space

    def ActionSpaceSample(self) -> Any:
        return self.env.action_space.sample()

    def Reset(self) -> Tuple[Any, Dict[str, Any]]:
        return self.env.reset()

    def Step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        return self.env.step(action)

    def Close(self):
        self.env.close()

    def SetScenario(self, scenario):
        self.env.scenario = scenario

    def GetScenario(self):
        if self.env.scenario is None:
            return Scenario({
                "dummy": 0
            })

        return self.env.scenario

    def SetRewardFunc(self, reward_func):
        self.env.set_reward_func(reward_func)

    def SetRenderMode(self, render_mode):
        self.env.render_mode = render_mode

    def GetRenderMode(self):
        return self.env.render_mode

    def GetRender(self):
        return self.env.render_frame()
