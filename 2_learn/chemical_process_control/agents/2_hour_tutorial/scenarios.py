# Scenarios
# Cref_signal is a configuration variable for Concentration and Temperature setpoints

#This is the scenario for the first skill Start Reaction of the industrial mixer.
#Scenarios are situations where your agent needs to behave differently to succeed. This example is introducting a 1% noise to the reaction.
#Copy this piece of code 2 times and re-name them to reflect the second and third skills in the agent design.
#You can use these 3 Cref_signal scenarios to train the agent to react to different setpoints: "ss1", "ss2", "transition", "complete"
# ss1 is the start_reaction
# ss2 is the produce product
# transition is the transition from start_reaction to produce product
# complete is to run all scenarios at once
start_reaction_scenarios = [
    {
        "Cref_signal": "ss1",
        "noise_percentage": 0.01
    }
]

transition_scenarios = [
    {
        "Cref_signal": "transition",
        "noise_percentage": 0.01
    }
]

produce_product_scenarios = [
    {
        "Cref_signal": "ss2",
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
