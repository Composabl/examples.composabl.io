import os

license_key = os.environ["COMPOSABL_KEY"]

config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-starship"
            },
            #"local": {
            #   "address": "localhost:1337"
            #}
        },
        "env": {
            "name": "starship",
        },
        "training": {},
        "runtime": {
            "workers": 1
        }
    }
