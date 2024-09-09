# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from composabl_core import Agent, Skill, Perceptor
from composabl import Trainer

from perceptor import TextPerceptor
from sensors import sensors_text
from teacher import TextTeacher
from sim import Sim

counter_skill = Skill("counter", TextTeacher)
counter_perceptor = Perceptor("counter_reversal", TextPerceptor)
agent = Agent()
agent.add_skill(counter_skill)
agent.add_perceptor(counter_perceptor)
agent.add_sensors(sensors_text)

config = {
    "license": "",
    "target": {
        "local": {
            "address": "localhost:1337"
        }
    },
    "env": {
        "name": "composabl",
    },
}

trainer = Trainer(config)

trainer.train(agent, train_cycles=1)

agent.export("agent.json")
agent = Agent.load("agent.json")

trainer.train(agent, train_cycles=2)

sim = Sim()
packaged_agent = trainer.package(agent)

for episode_idx in range(5):
    print("Episode: ", episode_idx)
    observation, info = sim.reset()
    done = False
    while not done:
        print("\tObservation: ", observation)
        action = packaged_agent.execute(observation)
        print("\tAction: ", action)
        observation, reward, done, _, info = sim.step(action)
        if done:
            break
