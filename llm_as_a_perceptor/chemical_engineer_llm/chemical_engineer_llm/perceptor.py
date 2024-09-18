# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from fake_llm import llm_client
from composabl_core import PerceptorImpl

class TextPerceptor(PerceptorImpl):
    """
    The perceptor for the text agent
    """
    def __init__(self, *args, **kwargs):
        self.llm_client = llm_client()
        pass

    async def compute(self, obs_spec, obs):
        """
        Asks the LLM for its thoughts on the current state of the plant, and returns a recommended action
        """
        llm_response = self.llm_client.ask(f"You are controlling a CSTR plant, the current state of the plant is {obs}. what action do you recommend?")
        llm_action = llm_response.find("action")
        return {"chemical_engineer_llm": llm_action}
    
    def filtered_sensor_space(self, obs):
        """
        Return the Sensor space part that is needed
        """
        raise ["state"]

