from composabl import Perceptor, Scenario
from sensors import sensors

class DemandPredict():
    def __init__(self):
        pass

    def compute(self, obs):  
        #Heuristic
        #co = int(round(1.3 * obs["cookies_demand"],0))
        #cp = int(round(1.1 * obs["cupcake_demand"]),0)
        #ck = int(round(1.05 * obs["cake_demand"]),0)
        co = 3
        
        #return {"cookies_demand_predict": co, "cupcake_demand_predict": cp, "cake_demand_predict": ck}
        return {"cookies_demand_predict": co}
    
    def filtered_observation_space(self, obs):
        return [s.name for s in sensors]


#co_predict = Perceptor("cookies_demand_predict", DemandPredict, "")
#cp_predict = Perceptor("cupcake_demand_predict", DemandPredict, "")
#ck_predict = Perceptor("cake_demand_predict", DemandPredict, "")
demand_predict = Perceptor("cookies_demand_predict", DemandPredict, "")

perceptors = [demand_predict]