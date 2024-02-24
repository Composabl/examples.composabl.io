from composabl import Perceptor, Scenario
from sensors import sensors

location_type = 0 #Location type: 0 = Urban, 1 = Suburban, 2 = near School
demand = "MED"
time = 0
day = 0
#Time of Day (time)
#0 = 9am (start of day)
#480 = 5pm (end of day)

#Day of week (day)
#0 = Monday, 6 = Sunday

base_demand_cookies = [60,100,100,120,200,250,250]
base_demand_cupcakes = [12,80,60,90,150,200,200]
base_demand_cakes = [2,50,50,60,100,125,150]

demand_modifier = { "HIGH" : 1.5, "MED" : 1.0, "LOW" : 0.50 }

class DemandPredict():
    def __init__(self):
        pass

    def compute(self, obs):  
        forcast = 0

        if location_type == 0:      #Urban bakery demand

            if time < 120:          #Opening to 11am
                demand = "LOW"
            if 120 <= time < 240:   #11am to 1pm, lunch rush
                demand = "HIGH"
            if 240 <= time < 420:   #1pm to 4pm
                demand = "LOW"
            if time >= 420:         #4pm to close, end of day rush
                demand = "MED" 

        if location_type == 1:      #Suburban bakery demand

            if time < 60:          #Opening to 10am, morning rush
                demand = "HIGH"
            if 60 <= time < 120:   #10am to 11am, late morning slump
                demand = "LOW"
            if 120 <= time < 240:   #11am to 1pm, lunch rush
                demand = "HIGH"
            if time >= 240:         #1pm to close, end of day demand
                demand = "MED" 

        if location_type == 2:      #School bakery demand

            if time < 240:          #Opening to 1pm
                demand = "LOW"
            if 240 <= time < 360:   #1pm to 3pm, after school rush
                demand = "HIGH"
            if time >= 360:         #3pm to close, end of day slump
                demand = "LOW" 

        forcast = demand_modifier[demand] #Right now return a basic value 
        
    #    forcast = [base_demand_cookies[day], base_demand_cupcakes[day], base_demand_cakes[day]]
    #    forcast = [demand_modifier[demand] * x for x in forcast]
        
        return {"demand_predict": forcast}
    
    def filtered_observation_space(self, obs):
        return [s.name for s in sensors]


ml_predict = Perceptor("demand_predict", DemandPredict, "")

perceptors = [ml_predict]