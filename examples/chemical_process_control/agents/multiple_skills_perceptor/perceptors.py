import os

from composabl import Perceptor, PerceptorImpl
import pickle

PATH = os.path.dirname(os.path.realpath(__file__))

class ThermalRunawayPredict(PerceptorImpl):
    def __init__(self):
        self.y = 0
        self.thermal_run = 0
        self.ml_model = pickle.load(open(f"{PATH}/ml_models/ml_predict_temperature.pkl", 'rb'))
        self.ML_list = []
        self.last_Tc = 0

    def compute(self, obs):
        #get the action - add action to perception
        #self.ΔTc = action[0]
        if self.last_Tc == 0:
            self.ΔTc = 5
        else:
            self.ΔTc = float(obs['Tc']) - self.last_Tc

        y = 0

        if obs['T'] >= 340:
            X = [[float(obs['Ca']), float(obs['T']), float(obs['Tc']), self.ΔTc]]
            y = self.ml_model.predict(X)[0]
            #print(self.ml_model.predict_proba(X))
            if self.ml_model.predict_proba(X)[0][1] >= 0.3:
                y = 1
                self.y = y

        self.last_Tc = float(obs['Tc'])

        return {"thermal_runaway_predict": y}

    def filtered_observation_space(self, obs):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']


ml_predict = Perceptor("thermal_runaway_predict", ThermalRunawayPredict, "Predict thermal runaway using a machine learning model.")

perceptors = [ml_predict]
