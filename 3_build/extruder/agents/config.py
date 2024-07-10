import os

license_key = os.environ["COMPOSABL_LICENSE"]

config = {
        "license": license_key,
        "target": {
            #"kubernetes": {
            #    "is_dev": True,
            #    "image": "octaviocomposabl/sim-rocket-landing:latest",
                #"sim_cpu": "1",
                #"sim_memory": "512Mi",
            #},
            "docker": {"image": "composabl/sim-filament-extruder"},
            #"local": {"address": "localhost:1337"}
        },
        "env": {
            "name": "filament-extruder",
        },
        "training": {},
        "trainer": {
            "workers": 8,
            "rollout_fragment_length": 60
        }
    }
