from composabl import Perceptor
import pickle

from cstr.external_sim.sim import CSTREnv


class ThermalRunawayPredict():
    def __init__(self):
        self.y = 0
        self.thermal_run = 0
        self.ml_model = pickle.load(open('./cstr/multiple_skills_perceptor/ml_models/ml_predict_temperature.pkl', 'rb'))
        self.ML_list = []

        self.sim = CSTREnv()
        obs, info = self.sim.reset()

    def compute(self, obs):   
        #get the action - add action to perception  
        #self.ΔTc = action[0]
        self.ΔTc = 5
        y = 0

        if obs['T'] >= 340:
            X = [[obs['Ca'], obs['T'], obs['Tc'], self.ΔTc]]
            y = self.ml_model.predict(X)[0]
            #print(self.ml_model.predict_proba(X))
            if self.ml_model.predict_proba(X)[0][1] >= 0.3:
                y = 1
                self.y = y
        
        return {"thermal_runaway_predict": y}
    
    def filtered_observation_space(self, obs):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']


ml_predict = Perceptor(["thermal_runaway_predict"], ThermalRunawayPredict, "")

perceptors = [ml_predict]