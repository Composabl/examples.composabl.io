from composabl import Perceptor


class PerceptorPredictThermalRunaway(Perceptor):
    def __init__(self):
        self.last_Tc = 0

    def compute(self, obs):
        # Compute the thermal runaway prediction based on observations

        # Set a default ΔTc if the last_Tc is not available
        if self.last_Tc == 0:
            self.ΔTc = 5
        else:
            self.ΔTc = obs["Tc"] - self.last_Tc

        y = 0

        # Check conditions for potential thermal runaway without ML model
        if obs["T"] >= 340:
            # Adjust the prediction based on a threshold condition
            if self.ΔTc >= 10:  # Define your threshold for runaway here
                y = 1
                self.y = y

        self.last_Tc = obs["Tc"]

        return {"thermal_runaway_predict": y}

    def filtered_observation_space(self, obs):
        # Define the observation space used by this perceptor
        return ["T", "Tc", "Ca", "Cref", "Tref"]
