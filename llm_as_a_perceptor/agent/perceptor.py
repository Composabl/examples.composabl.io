from composabl_core import PerceptorImpl

class TextPerceptor(PerceptorImpl):
    """
    The perceptor for the text agent
    """
    def __init__(self, *args, **kwargs):
        pass

    async def compute(self, obs_spec, obs):
        """
        Reverses the string of the text sensor
        """
        # print("Perceptor compute obs: ", obs)
        return {"text_reversed": obs["text"][::-1]}
    
    def filtered_sensor_space(self, obs):
        """
        Return the Sensor space part that is needed
        """
        raise ["text", "counter"]