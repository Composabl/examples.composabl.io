# README

This is a template for creating a new Perceptor. A Perceptor is a component that is responsible for processing data and returning a result. This can be used for example in a Machine Learning model, where the Perceptor is responsible for processing the data and returning the prediction.

## Tree Structure

The template is structured as follows:

```bash
my-perceptor/           # Root folder
├── my_perceptor/       # Main package folder
│   ├── __init__.py     # Package init file
│   └── perceptor.py    # Main perceptor file
├── pyproject.toml      # Project configuration, containing [composabl]
```

## PyProject [composabl] Section

We add the `[composabl]` section to the `pyproject.toml` file to specify the type of component we are creating as well as its entrypoint. This is used by the Composabl CLI to determine the type of
component and how to handle it.

Example:

```
[composabl]
type = "teacher"
entrypoint = "my_perceptor.perceptor:MyPerceptor"
```

## Development

To work on the Perceptor, you can simply create a temporary file or main file that starts up and executes the `compute` method of the portable Perceptor. Example, we can create a `test.py` file with:

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
pip install -e my-perceptor

# Run the test file
python my-perceptor/test.py
```

### Preparing for Upload

Once we are ready for uploading, we can create a `.tar.gz` file that contains the version. This can be done with the following command:

```bash
# Tar GZ the plugin
tar -czvf my-perceptor-0.0.1.tar.gz my-perceptor
```
