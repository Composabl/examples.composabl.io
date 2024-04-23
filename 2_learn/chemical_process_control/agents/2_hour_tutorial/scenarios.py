# Scenarios
# Cref_signal is a configuration variable for Concentration and Temperature setpoints

#This is the scenario for the first skill Start Reaction of the industrial mixer.
#Scenarios are situations where your agent needs to behave differently to succeed. This example is introducting a 1% noise to the reaction.
#Copy this piece of code 2 times and re-name them to reflect the second and third skills in the agent design.
start_reaction_scenarios = [
    {
        "Cref_signal": "start_reaction",
        "noise_percentage": 0.01
    }
]
# This is the scenario for the learned selector in the strategy pattern agent design.
selector_scenarios = [
    {
        "Cref_signal": "complete",
        "noise_percentage": 0.01
    }
]
