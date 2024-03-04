from composabl import Perceptor, Scenario
from sensors import sensors

class DemandPredict():
    def __init__(self):
        pass

    def compute(self, obs):  
        y = 0
        
        return {"demand_predict": y}
    
    def filtered_observation_space(self, obs):
        return [s.name for s in sensors]


ml_predict = Perceptor("demand_predict", DemandPredict, "")

perceptors = [ml_predict]