from composabl import Perceptor, Scenario
from sensors import sensors

class DemandPredict():
    def __init__(self):
        pass

    def compute(self, obs): 
        #Heuristic
        co = int(1.3 * obs["cookies_demand"])
        cp = int(1.1 * obs["cupcake_demand"])
        ck = int(1.05 * obs["cake_demand"])
        
        return {"cookies_demand_predict": co, "cupcake_demand_predict": cp, "cake_demand_predict": ck}
    
    def filtered_observation_space(self, obs):
        return [s.name for s in sensors]


demand_predict = Perceptor("demand_predict", DemandPredict, "")

perceptors = [demand_predict]