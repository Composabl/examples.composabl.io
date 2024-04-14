from abc import ABC, abstractmethod
import array
from cgitb import reset
from contextlib import nullcontext
import string
from typing import Dict, Any

import numpy as np

#from bakery_sim import BakerySim
from .bakery_sim import BakerySim
from .equipment import EquipmentNames
from .task import Task
from .recipe import RecipeNames
from .state import State


import simpy
import random

class Controller(ABC):
    
    yield_time = 1
    masking = []
    MAX_TIME = 480

    def __init__(self,env,debug=False):
        self.RESET_TIME = 1 
        self.env = env
        self.bakery_state = State(self.env, self.MAX_TIME)
        self.bakery_sim = BakerySim()
        self.equipment_store = simpy.FilterStore(self.env, capacity=7)
        self.equipment_store.items = [
            self.bakery_state.mixer_1,
            self.bakery_state.mixer_2,
            self.bakery_state.oven_1,
            self.bakery_state.oven_2,
            self.bakery_state.oven_3,
            self.bakery_state.decorating_station_1,
            self.bakery_state.decorating_station_2
        ]

        self.baker_store = simpy.FilterStore(self.env, capacity=4)
        self.baker_store.items = [
            self.bakery_state.baker_1,
            self.bakery_state.baker_2,
            self.bakery_state.baker_3,
            self.bakery_state.baker_4
        ]
        self.debug = debug

    @abstractmethod
    def step(self, action):
        pass
    @abstractmethod
    def get_mask(self):
        pass
    @abstractmethod
    def get_state(self):
        pass
    @abstractmethod
    def reset(self,config):
        pass

    def move_to_dessert_case(self,recipeName):
        if recipeName.value == RecipeNames.cookies.value:
            self.bakery_state.dessert_case_cookies += 12
        if recipeName.value == RecipeNames.cupcakes.value:
            self.bakery_state.dessert_case_cupcakes += 6
        if recipeName.value == RecipeNames.cake.value:
            self.bakery_state.dessert_case_cakes += 1
            
    def set_recipe_baker_and_dependency(self,equipment,baker,dependency) -> Dict[str, Any]:
        if equipment == EquipmentNames.mixer_1:
            if self.bakery_state.mixer_1.current_recipe.name != RecipeNames.none:
                recipe = self.bakery_state.mixer_1.current_recipe
            else:
                recipe = RecipeNames.none
            
        if equipment == EquipmentNames.mixer_2:
            if self.bakery_state.mixer_2.current_recipe.name != RecipeNames.none:
                recipe = self.bakery_state.mixer_2.current_recipe
            else:
                recipe = RecipeNames.none
        
        if equipment == EquipmentNames.oven_1:
            if self.bakery_state.oven_1.current_recipe.name != RecipeNames.none:
                recipe = self.bakery_state.oven_1.current_recipe
            else:
                recipe = RecipeNames.none
        
        if equipment == EquipmentNames.oven_2:
            if self.bakery_state.oven_2.current_recipe.name != RecipeNames.none:
                recipe = self.bakery_state.oven_2.current_recipe
            else:
                recipe = RecipeNames.none

        if equipment == EquipmentNames.oven_3:
            if self.bakery_state.oven_3.current_recipe.name != RecipeNames.none:
                recipe = self.bakery_state.oven_3.current_recipe
            else:
                recipe = RecipeNames.none
            
        recipe_baker_and_dependency_dict = {}
        recipe_baker_and_dependency_dict["recipe"] = recipe
        recipe_baker_and_dependency_dict["baker"] = baker
        recipe_baker_and_dependency_dict["dependency"] = dependency
        return recipe_baker_and_dependency_dict

    def set_recipe_and_baker(self,recipe,baker) -> Dict[str, Any]:
        recipe_and_baker_dict = {}
        recipe_and_baker_dict["recipe"] = recipe
        recipe_and_baker_dict["baker"] = baker
        return recipe_and_baker_dict

    def map_action_to_statement(self,action) -> string:
        action_string = "wait"
        if action == 1:
            action_string = "Chip_mix_cookies"
        if action == 2:
            action_string = "Chip_mix_cupcakes"
        if action == 3:
            action_string = "Chip_mix_cakes"
        if action == 4:
            action_string = "Coco_mix_cookies"
        if action == 5:
            action_string = "Coco_mix_cupcakes"
        if action == 6:
            action_string = "Coco_mix_cakes"
        if action == 7:
            action_string = "Eclair_mix_cookies"
        if action == 8:
            action_string = "Eclair_mix_cupcakes"
        if action == 9:
            action_string = "Eclair_mix_cakes"
        if action == 10:
            action_string = "Chip_bake_from_Mixer_1"
        if action == 11:
            action_string = "Chip_bake_from_Mixer_2"
        if action == 12:
            action_string = "Coco_bake_from_Mixer_1"
        if action == 13:
            action_string = "Coco_bake_from_Mixer_2"
        if action == 14:
            action_string = "Eclair_bake_from_Mixer_1"
        if action == 15:
            action_string = "Eclair_bake_from_Mixer_2"
        if action == 16:
            action_string = "Chip_decorate_from_Oven_1"
        if action == 17:
            action_string = "Chip_decorate_from_Oven_2"
        if action == 18:
            action_string = "Chip_decorate_from_Oven_3"
        if action == 19:
            action_string = "Eclair_decorate_from_Oven_1"
        if action == 20:
            action_string = "Eclair_decorate_from_Oven_2"
        if action == 21:
            action_string = "Eclair_decorate_from_Oven_3"
        if action == 22:
            action_string = "Reese_decorate_from_Oven_1"
        if action == 23:
            action_string = "Reese_decorate_from_Oven_2"
        if action == 24:
            action_string = "Reese_decorate_from_Oven_3"
        
        return action_string