from composabl import Perceptor, Scenario
from sensors import sensors

class DemandPredict():
    def __init__(self):
        pass

    def compute(self, obs):  
        #Heuristic
        co = int(round(1.3 * obs["cookies_demand"],0))
        cp = int(round(1.1 * obs["cupcake_demand"]),0)
        ck = int(round(1.05 * obs["cake_demand"]),0)
        
        return {"cookies_demand_predict": co, "cupcake_demand_predict": cp, "cake_demand_predict": ck}
    
    def filtered_observation_space(self, obs):
        return [s.name for s in sensors]


co_predict = Perceptor("cookies_demand_predict", DemandPredict, "")
cp_predict = Perceptor("cupcake_demand_predict", DemandPredict, "")
ck_predict = Perceptor("cake_demand_predict", DemandPredict, "")

perceptors = [co_predict, cp_predict, ck_predict]