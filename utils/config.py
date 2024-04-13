"""
Utils for generating config parameters for the agents.
"""

from typing import Any, Dict


def generate_config(
    license_key: str,
    target: str,
    image: str,
    env_name: str,
    workers: int,
    num_gpus: int = 0,
    **env_kwargs,
) -> Dict[str, Any]:
    """
    Generate config parameters for the agents.

    Args:
        license_key (str): License key.
        target (str): Target for the agent. Can be 'docker', 'local' or
            'kubernetes'.
        image (str): Docker image to be used.
        local_address (str): Local address.
        env_name (str): Name of the environment.
        workers (int): Number of workers.
        **kwargs: Additional parameters.

    Returns:
        dict: Config parameters for the agents.
    """

    env_kwargs = env_kwargs or {}

    config = {
        "license": license_key,
        "env": {
            "name": env_name,
            **env_kwargs,
        },
        "runtime": {
            "workers": workers,
            "num_gpus": num_gpus,
        }
    }

    if target == "docker":
        config["target"] = {
            "docker": {
                "image": image,
            }
        }

    elif target == "local":
        config["target"] = {
            "local": {
                "address": "localhost:1337",
            }
        }
        config["runtime"]["workers"] = 1
        config["runtime"]["num_gpus"] = 0

    elif target == "kubernetes":
        config["target"] = {
            "kubernetes": {
                "is_dev": True,
                "image": image,
                "output_dir": "/data",
            },
            "config": {
                "watchdog_timeout": 180,
            }
        }
        config["runtime"]["model"] = {
            "checkpoint_path": "/checkpoints",
        }

    return config
