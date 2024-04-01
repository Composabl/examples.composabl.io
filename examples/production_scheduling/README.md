# Whisky Business

Whisky Business Bakery Sim is a discrete event simulation developed in Python with the SimPy library.

There are two mixers, three ovens, two decoration stations and four bakers.

Each baker can only complete certain tasks during their shifts.

The simulation creates cupcakes, cakes, and cookies.

## How to start

Install your composabl package.
Composabl version :

```bash
pip install composabl-dev==0.6.2.dev25 composabl-cli-dev==0.6.2.dev25 composabl-core-dev==0.6.2.dev25 composabl-train-dev==0.6.2.dev25
```

## Train your agent

### Build and run the simulator image

#### Building and running

Go to the simulator folder

```bash
cd composabl/simulation
```

Build the simulator

```bash
docker build -t composabl/sim-whisky .
docker run --rm -it -p 1337:1337 composabl/sim-whisky
```

#### Running from Remote

```bash
docker pull composabl/sim-whisky
docker run --rm -it -p 1337:1337 composabl/sim-whisky
```

### Run the training code

```bash
python agent.py
```

### Analyze your training

train_history_analytics.ipynb

## Run your pre-trained agent

Your pre trained agent will be saved in the "checkpoints" folder. You can load your agent to continue the training or to run inference.

1. Run your simulation container
2. Run the inference code

```bash
python agent_inference.py
```


## References
- Composabl Docs: https://docs.composabl.io/
