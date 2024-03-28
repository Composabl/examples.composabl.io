# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import time
from composabl_core import PerceptorImpl


class DerivativePerceptor(PerceptorImpl):
    def __init__(self):
        self.previous_value = None
        self.previous_time = None

    async def compute(self, obs_spec, obs):
        current_value = obs["counter"]
        current_time = time.time()  # Get current time
        value_derived = 0

        # Only calculate derivative if we have a previous observation
        if self.previous_value is not None and self.previous_time is not None:
            time_delta = current_time - self.previous_time

            if time_delta > 0:  # Check to ensure time has passed
                value_derived = (current_value - self.previous_value) / time_delta

        # Update previous value and time for the next observation
        self.previous_value = current_value
        self.previous_time = current_time

        return {"counter_derived": value_derived}

    def filtered_observation_space(self, obs):
        return ["counter"]
