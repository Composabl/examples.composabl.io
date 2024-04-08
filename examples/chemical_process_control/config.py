import os

license_key = os.environ["COMPOSABL_KEY"]

config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-cstr-local:latest"
            },
            #"local": {
            #   "address": "localhost:1337"
            #}
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "workers": 2,
            "num_gpus": 0
        }
    }
