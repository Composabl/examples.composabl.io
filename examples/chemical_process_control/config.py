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


config_kub = {
        "license": license_key,
        "target": {
            "kubernetes": {
                "is_dev": True,
                "image": "composabl/sim-cstr:latest",
                #"output_dir": "/data",
            },
            "config": {
                "watchdog_timeout": 180,
            }
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "workers": 2,
            "num_gpus": 0,
            "model": {
                "checkpoint_path": "/tmp/checkpoint_cstr",
            }
        }
    }
