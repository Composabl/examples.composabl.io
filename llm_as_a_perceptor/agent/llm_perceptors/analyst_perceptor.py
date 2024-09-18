from fake_llm import llm_client
from fake_factory_console import factory_console_client

from composabl_core import PerceptorImpl

class AnalystPerceptor(PerceptorImpl):
    """
    The analyst type that displays information to the human operators but doesn't send any information to the agent.
    """
    def __init__(self, *args, **kwargs):
        # Example:
        self.llm_client = llm_client()
        self.factory_console_client = factory_console_client()
        pass

    async def compute(self, obs_spec, obs):       
        # First, ask the LLM for its thoughts on the current state of the plant
        llm_response = self.llm_client.ask(f"You are controlling a CSTR plant, the current state of the plant is {obs}. What are your thoughts on the current state of the plant?")

        # Second, post the LLM's thoughts to the factory console for a human to read
        self.factory_console_client.post(f"The LLM thoughts on the current state of the plant are: {llm_response}")

        return {"chemical_engineer_llm": 0}
    
    
    def filtered_sensor_space(self, obs):
        """
        Return the Sensor space part that is needed
        """
        raise ["counter"]
