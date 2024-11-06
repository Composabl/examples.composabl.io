# README

## Tree Structure

The template is structured as follows:

```bash
my-sim/                 # Root folder
├── my_sim/             # Main package folder
│   ├── __init__.py     # Package init file
│   ├── sim_impl.py     # Sim Implementation
│   └── sim.py          # Sim Itself
├── pyproject.toml      # Project configuration, containing [composabl]
```

## PyProject [composabl] Section

We add the `[composabl]` section to the `pyproject.toml` file to specify the sim we are creating as well as its entrypoint. This is used by the Composabl Sim Container to determine how to start the sim.

Example:

```toml
[composabl]
type = "sim"
entrypoint = "my_sim.sim_impl:MySimImpl"
```

## Development

To work on the Sim, you can simply run `composabl sim run <folder>`. This will do the same but locally.

## Preparing for Upload

Once we are ready for uploading, we can create a `.zip` file that contains the version and is prefixed with `composabl-sim-`. This can be done with the following command:

```bash
# Zip the Sim
zip -r composabl-sim-demo-0.0.1.zip sim-demo/
```
