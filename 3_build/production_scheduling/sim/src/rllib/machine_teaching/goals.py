from abc import ABC, abstractmethod

class Goal(ABC):

    @abstractmethod
    def reward_fn(self) -> float:
        """Reward function, passed into the environment, run at the end of each step"""

    @abstractmethod
    def terminate_fn(self) -> bool:
        """Terminate Function, passed into the environment, run at the end of each step"""
        
    @abstractmethod
    def step_metric(self,worker) -> float:
        """Store step metric value"""

    @abstractmethod
    def episode_success(self) -> bool:
        """Evaluate step metric value at the end of the episode for success"""
