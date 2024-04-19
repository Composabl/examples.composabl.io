import os

license_key = os.environ["COMPOSABL_LICENSE"]

config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-cstr:latest"
            },
            #"local": {
              # "address": "localhost:1337"
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
