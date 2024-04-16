import os

license_key = os.environ["COMPOSABL_LICENSE"]

config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-whisky-local:latest"
            },
            #"local": {
            #   "address": "localhost:1337"
            #}
        },
        "env": {
            "name": "sim-whisky",
        },
        "runtime": {
            "workers": 1,
            "num_gpus": 0
        }
    }
