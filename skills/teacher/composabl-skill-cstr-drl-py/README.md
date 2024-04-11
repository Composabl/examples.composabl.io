# README

## CLI

> Coming soon

## Getting Started

### Creating a new Portable Skill

To create a new Portable Skill, we need to adhere to the API specification as defined in `from composabl_core import SkillTeacher|SkillCoach|SkillController`. You create a Python module as you typically would, together with adding a section `[composabl]` to the `pyproject.toml`. An example Portable Skill will thus have the following folder structure:

```bash
my-skill/
├── my_skill/
│   ├── __init__.py
│   ├── controller.py
│   ├── coach.py
│   └── teacher.py
├── pyproject.toml
```

With the `pyproject.toml` file containing the following:

```toml
[project]
name = "composabl-skill-cstr-drl-py"
version = "0.1.0"
description = "A Composabl Demo Portable Teacher Skill"
authors = [{ name = "Xavier Geerinck", email = "xavier@composabl.io" }]
dependencies = [
    "composabl-core"
]

[composabl]
type = "teacher"
entrypoint = "composabl_skill_cstr_drl_py.teacher:Teacher"
```

### Development

To work on the Portable Skill, you can simply create a temporary file or main file that starts up and executes the `compute_reward` method (or any other) of the portable skill. Example, we can create a `test.py` file with:

```python
from composabl_skill_cstr_drl_py.teacher import Teacher


async def start():
    t = Teacher()
    reward = await t.compute_reward([], 1, 1.0)
    print(reward)


if __name__ == "__main__":
    import asyncio

    asyncio.run(start())
```

Which we can then run with

```bash
# Install the module
pip install -e composabl-skill-cstr-drl-py

# Run the test file
python composabl-skill-cstr-drl-py/test.py
```

### Preparing for Upload

Once we are ready for uploading, we can create a `.tar.gz` file that contains the version and is prefixed with `composabl-skill-`. This can be done with the following command:

```bash
# Tar GZ the plugin
tar -czvf composabl-skill-cstr-drl-py-0.0.1.tar.gz composabl-skill-cstr-drl-py
```
