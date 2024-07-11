import os

license_key = os.environ["COMPOSABL_LICENSE"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/model"

config = {
        "license": license_key,
        "target": {
            "kubernetes": {
                "is_dev": True,
                #"image": "octaviocomposabl/sim-rocket-landing:latest",
                "image": "composabl/sim-cstr-dev:latest",
                "sim_cpu": "1",
                "sim_memory": "512Mi",
            },
            #"docker": {"image": "composabl/sim-starship-local"},
            #"local": {"address": "localhost:1337"}
        },
        "env": {
            "name": "cstr",
        },
        "training": {},
        "trainer": {
            "workers": 1,
            #"model": {
            #    "checkpoint_path": PATH_CHECKPOINTS,
            #}
        }
    }
