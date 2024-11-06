import os

license_key = os.environ["COMPOSABL_LICENSE"]

config = {
    "license": license_key,
    "target": {
        "docker": {
            "image": "composabl/sim-inventory:latest"
        },
        #"local": {"address": "localhost:1337"}
    },
    "env": {
        "name": "inventory-management",
    },
    "trainer": {
        "workers": 8,
        "num_gpus": 0,
        #"rollout_fragment_length": 50
    },
    #"resources": {
    #        "env_runner_cpus": 4,
    #        "env_cpus": 1
    #    }
}
