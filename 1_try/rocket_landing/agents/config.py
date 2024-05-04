import os

license_key = os.environ["COMPOSABL_LICENSE"]

config = {
        "license": license_key,
        "target": {
             "docker": {
                 "image": "composabl/sim-starship-local"
             },
            #"local": {
            #  "address": "localhost:1337"
            #}
        },
        "env": {
            "name": "rocket-landing",
        },
        "training": {},
        "trainer": {
            "workers": 8
        }
    }
