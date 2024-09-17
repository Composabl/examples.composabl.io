# from fake_llm import llm_client
from composabl_core import PerceptorImpl

class TextPerceptor(PerceptorImpl):
    """
    The perceptor for the text agent
    """
    def __init__(self, *args, **kwargs):
        # Example:
        #self.llm_client = llm_client()
        pass

    async def compute(self, obs_spec, obs):
        """
        Reverses the string of the text sensor
        """
        # Example
        # response = self.llm_client(f"You are controlling a CSTR plant, the current state of the plant is {obs}. what action do you recommend?")
        # return {"chemical_engineer_llm": response}
        return {"text_reversed": obs["text"][::-1]}
    
    def filtered_sensor_space(self, obs):
        """
        Return the Sensor space part that is needed
        """
        raise ["text", "counter"]
