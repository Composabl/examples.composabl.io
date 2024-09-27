import asyncio
import os

from composabl import Agent, Trainer
import numpy as np

from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Global objects (initialized once)
trainer = None
trained_agent = None

license_key = os.environ["COMPOSABL_LICENSE"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_CHECKPOINTS = f"{PATH}/model/agent.json"

# Initialize the runtime, load the model, and package it when the app starts
async def init_runtime():
    """
    Initializes the trainer and agent before the first request is processed.
    This sets up the AI model for inference, loading it from checkpoints and preparing the agent.
    """
    global trainer, trained_agent

    # Assuming 'config' is required to initialize the Trainer
    config = {
        "license": license_key,
        "target": {
            "local": {"address": "localhost:1337"}
        },
        "env": {
            "name": "sim-deploy",
        },
        "trainer": {
            "workers": 1
        }
    }

    # Initialize the Trainer with the config
    trainer = Trainer(config)

    # Load the agent from the given checkpoint path
    agent = Agent.load(PATH_CHECKPOINTS)

    # Package the agent for inference using the Trainer's _package function (asynchronously)
    trained_agent = await trainer._package(agent)


# Asynchronous POST route to receive observation and return action
@app.route('/predict', methods=['POST'])
async def predict():
    """
    Receives an observation through a POST request, processes it using the pre-trained agent,
    and returns the corresponding action.
    """
    global trained_agent

    # Check if the agent has been successfully initialized
    if not trained_agent:
        return jsonify({"error": "Agent not initialized"}), 500

    # Extract the observation from the request's JSON body
    obs = request.json.get("observation")

    obs = dict(obs)
    obs = np.array( [float(x) for x in list(obs.values())] )

    # Validate that the observation was provided in the request
    if obs is None:
        return jsonify({"error": "No observation provided"}), 400

    # Asynchronously process the observation to generate the action
    action = await trained_agent._execute(obs)

    # Return the generated action in the response
    return jsonify({"action": str(action)})


if __name__ == "__main__":
    # Run the Flask application with async support on localhost, port 8000
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_runtime())

    app.run(host="0.0.0.0", port=8000, debug=True)
