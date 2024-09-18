from fake_llm import llm_client
from fake_factory_console import factory_console_client

from composabl_core import PerceptorImpl

class AnalystPerceptor(PerceptorImpl):
    """
    The executive/plant manager type that sends new sensor information to the agent based on either external information or natural language inputs from the operator.
    """
    def __init__(self, *args, **kwargs):
        # Example:
        self.llm_client = llm_client()
        self.factory_console_client = factory_console_client()
        pass

    async def compute(self, obs_spec, obs):
        # 1. First, get the input from the plant manager
        plant_manger_response = self.factory_console_client.post("What are your thoughts on the current state of the plant?")
        
        # 2. Ask the LLM for its thoughts on the current state of the plant
        llm_response = self.llm_client.ask(f"You are controlling a CSTR plant, the current state of the plant is {obs}. The plant manager has observed the following: {plant_manger_response}. What action would you recommend?")

        llm_action = llm_response.find("action")

        return {"chemical_engineer_llm": llm_action}
    
    
    def filtered_sensor_space(self, obs):
        """
        Return the Sensor space part that is needed
        """
        raise ["text", "counter"]
