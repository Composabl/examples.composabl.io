import array
import math
import simpy
from typing import Dict, Any
from .baker import Baker, BakerNames
from .recipe import Recipe, RecipeNames
from .equipment import Equipment, EquipmentNames


class State:

    def __init__(self, environment : simpy.Environment, sim_time : int):

        self.recipes = {
            RecipeNames.none : Recipe(RecipeNames.none, 0, 0, 0, 0),
            RecipeNames.cookies : Recipe(RecipeNames.cookies, 12, 5, 13, 10),
            RecipeNames.cupcakes : Recipe(RecipeNames.cupcakes, 6, 7, 30, 20),
            RecipeNames.cake : Recipe(RecipeNames.cake, 1, 10, 40, 30),
        }

        self.baker_1 = Baker(environment, sim_time, BakerNames.Chip, True, True, True, 0, sim_time)
        self.baker_2 = Baker(environment, sim_time, BakerNames.Coco, True, True, False, 0, sim_time)
        self.baker_3 = Baker(environment, sim_time, BakerNames.Eclair, True, True, True, 0, sim_time)
        self.baker_4 = Baker(environment, sim_time, BakerNames.Reese, True, False, False, 0, math.floor(sim_time / 2))

        self.mixer_1 = Equipment(EquipmentNames.mixer_1.name, environment)
        self.mixer_2 = Equipment(EquipmentNames.mixer_2.name, environment)
        self.oven_1 = Equipment(EquipmentNames.oven_1.name, environment)
        self.oven_2 = Equipment(EquipmentNames.oven_2.name, environment)
        self.oven_3 = Equipment(EquipmentNames.oven_3.name, environment)
        self.decorating_station_1 = Equipment(EquipmentNames.decorating_station_1.name, environment)
        self.decorating_station_2 = Equipment(EquipmentNames.decorating_station_2.name, environment)

        self.dessert_case_cookies : int = 0
        self.dessert_case_cupcakes : int = 0
        self.dessert_case_cakes : int = 0

        self._env = environment
        self._sim_time = sim_time

    def set_state(self, config : Dict[str, Any]) -> None:
        if config == {'nothing': None} :
            pass
        else:
            self._sim_time = config['sim_time'] 
            self.baker_1.busy_for = config['baker_1_time_remaining']
            self.baker_2.busy_for = config['baker_2_time_remaining']
            self.baker_3.busy_for = config['baker_3_time_remaining']
            self.baker_4.busy_for = config['baker_4_time_remaining']
            
            self.set_equipment(self.mixer_1, RecipeNames(config['mixer_1_recipe']), config['mixer_1_time_remaining'], 'mixer')
            self.set_equipment(self.mixer_2, RecipeNames(config['mixer_2_recipe']), config['mixer_2_time_remaining'], 'mixer')

            self.set_equipment(self.oven_1, RecipeNames(config['oven_1_recipe']), config['oven_1_time_remaining'], 'oven')
            self.set_equipment(self.oven_2, RecipeNames(config['oven_2_recipe']), config['oven_2_time_remaining'], 'oven')
            self.set_equipment(self.oven_3, RecipeNames(config['oven_3_recipe']), config['oven_3_time_remaining'], 'oven')

            self.set_equipment(self.decorating_station_1, RecipeNames(config['decorating_station_1_recipe']), config['decorating_station_1_time_remaining'], 'decorating_station')
            self.set_equipment(self.decorating_station_2, RecipeNames(config['decorating_station_2_recipe']), config['decorating_station_2_time_remaining'], 'decorating_station')

            self.dessert_case_cookies = config['completed_cookies'] 
            self.dessert_case_cupcakes = config['completed_cupcakes'] 
            self.dessert_case_cakes = config['completed_cake'] 

    def set_equipment(self, equipment:Equipment, recipe_name: RecipeNames, remaining_time:int, asset_class:str):        
        equipment.set_in_use(self.recipes[recipe_name],
                             (self._env.now - (equipment.current_recipe.times[asset_class] - remaining_time)),
                             remaining_time)

    def print_equipment(self) -> None:
        print('\nBAKERY EQUIPMENT')
        self.mixer_1.print_equipment()
        self.mixer_2.print_equipment()
        self.oven_1.print_equipment()
        self.oven_2.print_equipment()
        self.oven_3.print_equipment()
        self.decorating_station_1.print_equipment()
        self.decorating_station_2.print_equipment()

    def print_bakers(self) -> None:
        print('\nBAKERS')
        self.baker_1.print_baker()
        self.baker_2.print_baker()
        self.baker_3.print_baker()
        self.baker_4.print_baker()

    def print_dessert_case(self) -> None:
        print('\nDESSERT CASE')
        print(RecipeNames.cookies.name, self.dessert_case_cookies)
        print(RecipeNames.cupcakes.name, self.dessert_case_cupcakes)
        print(RecipeNames.cake.name, self.dessert_case_cakes)

    def get_state(self) -> Dict[str, Any]:
        return {

            #'time' : self._env.now,
            'sim_time' : self._sim_time,
            
            # BAKERS
            'baker_1_time_remaining' : self.baker_1.remaining_time(),
            'baker_2_time_remaining' : self.baker_2.remaining_time(),
            'baker_3_time_remaining' : self.baker_3.remaining_time(),
            'baker_4_time_remaining' : self.baker_4.remaining_time(),

            # EQUIPMENT
            'mixer_1_recipe' : self.mixer_1.current_recipe.name.value, #Issue here 
            'mixer_1_time_remaining' : self.mixer_1.time_remaining,
            'mixer_2_recipe' : self.mixer_2.current_recipe.name.value,
            'mixer_2_time_remaining' : self.mixer_2.time_remaining,

            'oven_1_recipe' : self.oven_1.current_recipe.name.value,
            'oven_1_time_remaining' : self.oven_1.time_remaining,
            'oven_2_recipe' : self.oven_2.current_recipe.name.value,
            'oven_2_time_remaining' : self.oven_2.time_remaining,
            'oven_3_recipe' : self.oven_3.current_recipe.name.value,
            'oven_3_time_remaining' : self.oven_3.time_remaining,

            'decorating_station_1_recipe' : self.decorating_station_1.current_recipe.name.value,
            'decorating_station_1_time_remaining' : self.decorating_station_1.time_remaining,
            'decorating_station_2_recipe' : self.decorating_station_2.current_recipe.name.value,
            'decorating_station_2_time_remaining' : self.decorating_station_2.time_remaining,

            # DESSERT CASE
            'completed_cookies' : self.dessert_case_cookies,
            'completed_cupcakes' : self.dessert_case_cupcakes,
            'completed_cake' : self.dessert_case_cakes,

        }
    
    def get_rllib_action(self) -> Dict[str, Any]:
        return {        
            "masking_array" : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        }

