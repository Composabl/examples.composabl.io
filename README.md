# Composabl Examples

This repository holds different examples for how you can get started with the Composabl SDK!

## Structure

- **agents/:** holds examples on how to train an agent
- **simulators/:** holds examples on how to create a custom simulator
- **docker/:** scripts used to create a dev container

## Getting Started

You can get started with an example by following the commands below:

```bash
# Start the historian
composabl historian start

# Start a sim
# e.g., composabl sim start sim-demo
composabl sim start sim-NAME

# Train an agent
# e.g., poetry run demo
cd agents/
export COMPOSABL_KEY="<YOUR_KEY>"
python cstr/agent.py
```

## Codespaces (Devcontainer)

A Codespace is available for use to test out the Composabl SDK. Just click the Code -> Codespaces -> + button

![](./images/demo-codespace.png)

## More Info

You can find more info on the Composabl SDK on our [Documentation](https://docs.composabl.io)
