# Agents

In this folder you can find all the different example agents we support:

- **Airplane:** Learn how to implement an autopilot on an airplane
- **Boiler:**
- **CSTR:**
- **Demo:**
- **Filament Extruder:**
- **Inventory:**
- **Lunar Lander:**
- **Maintenance:**
- **Starship:**

## Prerequisites

- [Poetry](https://python-poetry.org/docs/)

## Getting Started

To make it easy, we are using [Poetry](https://python-poetry.org/docs/) as a dependency management tool that allows us to easily start up any of the agents.

```bash
# Install Dependencies
poetry install

# Set your License Key
# if you do not have this, contact us at sales@composabl.io
export COMPOSABL_KEY="YOUR_KEY"

# Accept the EULA
# note: by adding this variable, you are agreeing to our EULA at https://composabl.io/legal/sdk-beta-agreement
export COMPOSABL_EULA_AGREED=1

# Run an agent
# e.g., poetry run airplane, poetry run boiler, poetry run cstr, ...
poetry run YOUR_AGENT
```
