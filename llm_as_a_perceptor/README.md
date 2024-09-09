# LLM As a Composabl Perceptor

This repo shows how to the Composabl SDK is able to process text information. 

In this example, part of the sim's observation space is of type `gym.Text`, as well as a perceptor whose output is of type `gym.Text`. 

The `Perceptor` simply reversed the string, however this can replaced by any API call to any LLM for every episode step of the training and inference process. 

The `SkillTeacher` validates that the sim's text and the perceptor text exist in the composabl observation space, and also that the perceptor's value is the string reversal of the sim's text. 

Lastly, all text fields in the composabl observation space must be filtered out via the `filtered_sensor_space` method of the teacher, since the Composabl SDK does not tokenize text automatically. 
