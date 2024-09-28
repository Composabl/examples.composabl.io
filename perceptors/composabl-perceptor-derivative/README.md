# README

## CLI

> Coming soon

## Getting Started

### Creating a new Portable Perceptor

To create a new Portable Perceptor, we need to adhere to the API specification as defined in `from composabl_core import PerceptorImpl`. You create a Python module as you typically would, together with adding a section `[composabl]` to the `pyproject.toml`. An example Portable Perceptor will thus have the following folder structure:

```bash
my-perceptor/
├── my_perceptor/
│   ├── __init__.py
│   └── perceptor.py
├── pyproject.toml
```

With the `pyproject.toml` file containing the following:

```toml
[project]
name = "composabl-perceptor-my-perceptor"
version = "0.1.0"
description = "A Composabl Demo Portable Perceptor"
authors = [{ name = "Xavier Geerinck", email = "xavier@composabl.io" }]
dependencies = [
    "composabl-core"
]

[composabl]
type = "teacher"
entrypoint = "my_perceptor.perceptor:MyPerceptor"
```

### Development

To work on the Portable Perceptor, you can simply create a temporary file or main file that starts up and executes the `compute` method of the portable Perceptor. Example, we can create a `test.py` file with:

```python
from composabl_perceptor_my_perceptor.perceptor import MyPerceptor


async def start():
    p = MyPerceptor()
    res = await t.compute(None, [1.0])
    print(res)


if __name__ == "__main__":
    import asyncio

    asyncio.run(start())
```

Which we can then run with

```bash
# Install the module
pip install -e composabl-perceptor-my-perceptor

# Run the test file
python composabl-perceptor-my-perceptor/test.py
```

### Preparing for Upload

Once we are ready for uploading, we can create a `.tar.gz` file that contains the version and is prefixed with `composabl-perceptor-`. This can be done with the following command:

```bash
# Tar GZ the plugin
tar -czvf composabl-perceptor-my-perceptor-0.0.1.tar.gz composabl-perceptor-my-perceptor
```
