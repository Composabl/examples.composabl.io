from abc import ABC, abstractmethod

class Assessment(ABC):
    @abstractmethod
    def scenarios(dict) -> float:
        """Scenarios for assessments"""
        
