from composabl import Scenario

bake_scenarios = [
        {   # High Demand
            "cookies_demand": 100,
            "cupcake_demand": 18,
            "cake_demand": 5,
        },
        {   # Std Demand
            "cookies_demand": 60,
            "cupcake_demand": 18,
            "cake_demand": 2,
        },
        {   # Low Demand
            "cookies_demand": 20,
            "cupcake_demand": 6,
            "cake_demand": 1,
        },
        {   # Xmas Demand
            "cookies_demand": 260,
            "cupcake_demand": 10,
            "cake_demand": 1,
        },
        {   # Cupcake Wars
            "cookies_demand": 0,
            "cupcake_demand": 96,
            "cake_demand": 0,
        },
        {   # Cookie Wars
            "cookies_demand": 396,
            "cupcake_demand": 0,
            "cake_demand": 0,
        },
        {   # November Birthday
            "cookies_demand": 0,
            "cupcake_demand": 0,
            "cake_demand": 11,
        }
    ]


# dt=1 minute, we are running for 8hours=480 mins
high_demand_scenarios = [
    {   # High Demand
        "cookies_demand": [60,100,120],
        "cupcake_demand": [18,30,40],
        "cake_demand": [5,7,10],
    }
]

low_demand_scenarios = [
    {   # Low Demand
        "cookies_demand": [10,20,50],
        "cupcake_demand": [6,10,15],
        "cake_demand": [1,3,4],
    },
]

normal_demand_scenarios = [
    {   # Std Demand
        "cookies_demand": 60,
        "cupcake_demand": 18,
        "cake_demand": 2,
    },
]

selector_scenarios = [
    {
        "cookies_demand": [10,20,30,50,70,80,100],
        "cupcake_demand": [6,10,15,18,20,25,30],
        "cake_demand": [1,3,5,6,7,10,11],
    }
]
