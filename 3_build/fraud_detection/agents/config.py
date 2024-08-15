import os

license_key = os.environ["COMPOSABL_LICENSE"]

config = {
    "license": license_key,
    "target": {
        "docker": {"image": "composabl/sim-fraud-local:latest"},
        # "local": {"address": "localhost:1337"},
    },
    "env": {
        "name": "sim-fraud-detection",
    },
    "trainer": {
        "rollout_fragment_length": 80,
        "workers": 1,
        "num_gpus": 0
    }
}
