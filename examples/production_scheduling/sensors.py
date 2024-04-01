from composabl import Sensor

step_action_dict = {
    0:"wait",
    1:"Chip_mix_cookies",
    2:"Chip_mix_cupcakes",
    3:"Chip_mix_cakes",
    4:"Coco_mix_cookies",
    5:"Coco_mix_cupcakes",
    6:"Coco_mix_cakes",
    7:"Eclair_mix_cookies",
    8:"Eclair_mix_cupcakes",
    9:"Eclair_mix_cakes",
    10:"Chip_bake_from_Mixer_1",
    11:"Chip_bake_from_Mixer_2",
    12:"Coco_bake_from_Mixer_1",
    13:"Coco_bake_from_Mixer_2",
    14:"Eclair_bake_from_Mixer_1",
    15:"Eclair_bake_from_Mixer_2",
    16:"Chip_decorate_from_Oven_1",
    17:"Chip_decorate_from_Oven_2",
    18:"Chip_decorate_from_Oven_3",
    19:"Eclair_decorate_from_Oven_1",
    20:"Eclair_decorate_from_Oven_2",
    21:"Eclair_decorate_from_Oven_3",
    22:"Reese_decorate_from_Oven_1",
    23:"Reese_decorate_from_Oven_2",
    24:"Reese_decorate_from_Oven_3"
}
observation_dict = {
    0:'sim_time',
    1:'baker_1_time_remaining',
    2:'baker_2_time_remaining',
    3:'baker_3_time_remaining',
    4:'baker_4_time_remaining',
    # EQUIPMENT
    5:'mixer_1_recipe',
    6:'mixer_1_time_remaining',
    7:'mixer_2_recipe',
    8:'mixer_2_time_remaining',
    9:'oven_1_recipe',
    10:'oven_1_time_remaining',
    11:'oven_2_recipe',
    12:'oven_2_time_remaining',
    13:'oven_3_recipe',
    14:'oven_3_time_remaining',
    15:'decorating_station_1_recipe',
    16:'decorating_station_1_time_remaining',
    17:'decorating_station_2_recipe',
    18:'decorating_station_2_time_remaining'
}

dessert_cases = {
    0:'completed_cookies',
    1:'completed_cupcakes',
    2:'completed_cake'
}

dessert_prices = {
    0:'cookies_price',
    1:'cupcake_price',
    2:'cake_price'
}

dessert_demand = {
    0:'cookies_demand',
    1:'cupcake_demand',
    2:'cake_demand'
}

dessert_cost = {
    0:'cookies_cost',
    1:'cupcake_cost',
    2:'cake_cost'
}

sensors_dict_list = [step_action_dict, observation_dict, dessert_cases, dessert_prices, dessert_demand, dessert_cost]

sensors = []
for d in sensors_dict_list:
    for key in list(d.keys()):
        globals()[d[key]] = Sensor(d[key], "")
        sensors.append(globals()[d[key]])