
import array
from cgitb import reset
from contextlib import nullcontext
import string
from typing import Dict, Any

import numpy as np

from .controller import Controller

#from bakery_sim import BakerySim
from .bakery_sim import BakerySim
from .equipment import EquipmentNames
from .task import Task
from .recipe import RecipeNames
from .state import State


import simpy
import random

yield_time = 1
masking = []
MAX_TIME = 480

class SimController(Controller):

    def __init__(
        self,
        env,
        debug
    ):
        self.RESET_TIME = 1 
        self.env = env
        self.bakery_state = State(self.env, MAX_TIME)
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

    def get_mask(self) -> array :
        masking_array = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        if self.bakery_state.baker_1.busy_for == None:
            self.bakery_state.baker_1.busy_for = 0

        if self.bakery_state.baker_1.busy_for > 0:
            masking_array[1] = 0
            masking_array[2] = 0  
            masking_array[3] = 0
            masking_array[10] = 0
            masking_array[11] = 0  
            masking_array[16] = 0  
            masking_array[17] = 0  
            masking_array[18] = 0    

        if self.bakery_state.baker_2.busy_for == None:
            self.bakery_state.baker_2.busy_for = 0

        if self.bakery_state.baker_2.busy_for  > 0:
            masking_array[4] = 0
            masking_array[5] = 0  
            masking_array[6] = 0
            masking_array[12] = 0
            masking_array[13] = 0  

        if self.bakery_state.baker_3.busy_for == None:
            self.bakery_state.baker_3.busy_for = 0

        if self.bakery_state.baker_3.busy_for > 0:
            masking_array[7] = 0
            masking_array[8] = 0  
            masking_array[9] = 0
            masking_array[14] = 0
            masking_array[15] = 0  
            masking_array[19] = 0  
            masking_array[20] = 0  
            masking_array[21] = 0 

        if self.bakery_state.baker_4.busy_for == None:
            self.bakery_state.baker_4.busy_for = 0

        if self.bakery_state.baker_4.busy_for > 0 or self.env.now < 240:
            masking_array[22] = 0
            masking_array[23] = 0  
            masking_array[24] = 0

        if self.bakery_state.mixer_1.current_recipe == None:
            self.bakery_state.mixer_1.current_recipe = RecipeNames(0)
        
        if self.bakery_state.mixer_2.current_recipe == None:
            self.bakery_state.mixer_2.current_recipe = RecipeNames(0)
        
        if self.bakery_state.oven_1.current_recipe == None:
            self.bakery_state.oven_1.current_recipe  = RecipeNames(0)
        
        if self.bakery_state.oven_2.current_recipe == None:
            self.bakery_state.oven_2.current_recipe  = RecipeNames(0)

        if self.bakery_state.oven_3.current_recipe == None:
            self.bakery_state.oven_3.current_recipe  = RecipeNames(0)

        if  self.bakery_state.mixer_1.current_recipe.name.value != 0 and self.bakery_state.mixer_2.current_recipe.name.value != 0:
            masking_array[1] = 0
            masking_array[2] = 0  
            masking_array[3] = 0
            masking_array[4] = 0
            masking_array[5] = 0  
            masking_array[6] = 0
            masking_array[7] = 0
            masking_array[8] = 0  
            masking_array[9] = 0
        
        if self.bakery_state.mixer_1.current_recipe.name.value == 0 or self.bakery_state.mixer_1.time_remaining > 0:
            masking_array[10] = 0
            masking_array[12] = 0
            masking_array[14] = 0

        if self.bakery_state.mixer_2.current_recipe.name.value == 0 or self.bakery_state.mixer_2.time_remaining > 0:
            masking_array[11] = 0
            masking_array[13] = 0
            masking_array[15] = 0

        if self.bakery_state.oven_1.current_recipe.name.value == 0 or self.bakery_state.oven_1.time_remaining > 0:
            masking_array[16] = 0
            masking_array[19] = 0
            masking_array[22] = 0

        if self.bakery_state.oven_2.current_recipe.name.value == 0 or self.bakery_state.oven_2.time_remaining > 0:
            masking_array[17] = 0
            masking_array[20] = 0
            masking_array[23] = 0

        if self.bakery_state.oven_3.current_recipe.name.value == 0 or self.bakery_state.oven_3.time_remaining > 0:
            masking_array[18] = 0
            masking_array[21] = 0
            masking_array[24] = 0
        
        return masking_array

    def reset(self,config) -> Dict[str, Any]:
        reset_state = self.bakery_sim.reset(config, self.bakery_state)

        self.env.run(until = self.RESET_TIME + self.env.now) 

        return reset_state

    def step(self,action) -> Dict[str, Any]: 
        action_string = self.map_action_to_statement(action["action"])
        baker = 0
        #self.bakery_state = sim_model_state_reset
        time = self.bakery_state._sim_time - yield_time

        if self.debug == True:
            print('BEFORE TIME', time)

        equipment = 0
        dependency = 0
        recipe = 0
        masking_array = []
        if time < 0:
            return {}

        if self.bakery_state.decorating_station_1.current_recipe != None:
          if self.bakery_state.decorating_station_1.current_recipe.name.value  > 0 and self.bakery_state.decorating_station_1.time_remaining == 0: 
            self.move_to_dessert_case(self.bakery_state.decorating_station_1.current_recipe.name)
            self.bakery_state.decorating_station_1.set_not_in_use()

        if self.bakery_state.decorating_station_2.current_recipe != None:
          if self.bakery_state.decorating_station_2.current_recipe.name.value > 0 and self.bakery_state.decorating_station_2.time_remaining == 0: 
            self.move_to_dessert_case(self.bakery_state.decorating_station_2.current_recipe.name)
            self.bakery_state.decorating_station_2.set_not_in_use()

        if action_string ==  "wait":
            self.env.run(until=yield_time + self.env.now)
            self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
            self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
            self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
            self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
            self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
            self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
            self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
            self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()

            if self.debug == True:
                print('yield_time =',yield_time)
                print('env =', self.env.now)
                print('CAN NOT COMPLETE ACTION; NO VALUES IN MIXER; TRY AGAIN')
                print('\ntime:', self.env.now)
                print('time remaining:', self.bakery_state._sim_time)

            self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
            
            masking_array = self.set_game_masking()

            action_array = self.map_masking_to_action(masking_array)

            return self.bonsai_get_sim_state(masking_array,action_array)

        elif action_string ==  "Chip_mix_cookies" or action_string == "Chip_mix_cupcakes" or action_string == "Chip_mix_cakes" or action_string == "Coco_mix_cookies" or action_string == "Coco_mix_cupcakes" or action_string == "Coco_mix_cakes" or action_string == "Eclair_mix_cookies" or action_string == "Eclair_mix_cupcakes" or action_string == "Eclair_mix_cakes": 

            if action_string ==  "Chip_mix_cookies":
                recipe_and_baker = self.set_recipe_and_baker(1,1)
            
            if action_string == "Chip_mix_cupcakes":
                recipe_and_baker = self.set_recipe_and_baker(2,1)
                
            if action_string == "Chip_mix_cakes":
                recipe_and_baker = self.set_recipe_and_baker(3,1)
            
            if action_string == "Coco_mix_cookies":
                recipe_and_baker = self.set_recipe_and_baker(1,2)

            if action_string == "Coco_mix_cupcakes":
                recipe_and_baker = self.set_recipe_and_baker(2,2)
            
            if action_string == "Coco_mix_cakes":
                recipe_and_baker = self.set_recipe_and_baker(3,2)

            if action_string == "Eclair_mix_cookies":
                recipe_and_baker = self.set_recipe_and_baker(1,3)
  
            if action_string == "Eclair_mix_cupcakes":
                recipe_and_baker = self.set_recipe_and_baker(2,3)
            
            if action_string == "Eclair_mix_cakes":
                recipe_and_baker = self.set_recipe_and_baker(3,3)

            if self.bakery_state.mixer_1.current_recipe.name == RecipeNames.none: 
                equipment = 1
            
            elif self.bakery_state.mixer_2.current_recipe.name == RecipeNames.none: 
                equipment = 2
            
            else:
                equipment = 0 #Waiting 
            
            dependency = 0 

            baker = recipe_and_baker["baker"]
            recipe = recipe_and_baker["recipe"]

            task_mixer = Task('mixer',baker,equipment,dependency)
 
            move_to_mixer_batch = {}
            move_to_mixer_batch["env"] = self.env
            move_to_mixer_batch["sim_time"] = self.bakery_state._sim_time
            move_to_mixer_batch["bakery_state"] = self.bakery_state
            move_to_mixer_batch["equipment"] = equipment
            move_to_mixer_batch["baker"] = baker
            move_to_mixer_batch["recipe"] = recipe
            move_to_mixer_batch["equipment_store"] = self.equipment_store
            move_to_mixer_batch["baker_store"] = self.baker_store
            move_to_mixer_batch["dependency"] = dependency
            move_to_mixer_batch["task_mixer"] = task_mixer

 
            self.env.process(self.bakery_sim.move_to_mixer(move_to_mixer_batch))
            print('yield_time =',yield_time)
            print('env =', self.env.now)
            self.env.run(until= yield_time + self.env.now)

            self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
            self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
            self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
            self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
            self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
            self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
            self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
            self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()
            
            print('\ntime:', self.env.now)
            print('time remaining:', self.bakery_state._sim_time)
            self.bakery_state.print_dessert_case()
            self.bakery_state.print_bakers()
            self.bakery_state.print_equipment()

            masking_array = self.set_game_masking()

            action_array = self.map_masking_to_action(masking_array)

            return self.bonsai_get_sim_state(masking_array,action_array)
            
        
        elif action_string == "Chip_bake_from_Mixer_1" or action_string == "Chip_bake_from_Mixer_2" or action_string == "Coco_bake_from_Mixer_1" or action_string == "Coco_bake_from_Mixer_2" or action_string == "Eclair_bake_from_Mixer_1" or action_string == "Eclair_bake_from_Mixer_2":
            if baker != 4:
                if self.bakery_state.mixer_1.current_recipe.name != RecipeNames.none or self.bakery_state.mixer_2.current_recipe.name != RecipeNames.none:                    
                    if action_string == "Chip_bake_from_Mixer_1":
                       recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.mixer_1,1,1)
                    
                    if action_string == "Chip_bake_from_Mixer_2":
                        recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.mixer_2,1,2)
                    
                    if action_string == "Coco_bake_from_Mixer_1":
                        recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.mixer_1,2,1)
                
                    if action_string == "Coco_bake_from_Mixer_2":
                        recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.mixer_2,2,2)

                    if action_string == "Eclair_bake_from_Mixer_1":
                        recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.mixer_1,3,1)

                    if action_string == "Eclair_bake_from_Mixer_2":
                        recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.mixer_2,3,2)

                    if (self.bakery_state.oven_1.current_recipe.name == RecipeNames.none or self.bakery_state.oven_1.current_recipe.name.value == 0):  #select oven 1 - 3
                        equipment = 3
                    
                    elif (self.bakery_state.oven_2.current_recipe.name == RecipeNames.none or self.bakery_state.oven_2.current_recipe.name.value == 0): #select oven 2 - 4
                        equipment = 4

                    elif (self.bakery_state.oven_3.current_recipe.name == RecipeNames.none or self.bakery_state.oven_3.current_recipe.name.value == 0): #select oven 3 - 5
                        equipment = 5
                    
                    else:
                        equipment = 0 #Waiting 

                    
                    baker = recipe_baker_and_dependency["baker"] #= baker
                    recipe = recipe_baker_and_dependency["recipe"].name.value #recipe_baker_and_dependency["recipe"] #= recipe
                    dependency = recipe_baker_and_dependency["dependency"] #= dependency

                    task_oven= Task('oven',baker,equipment,dependency)

                    move_to_oven_batch = {}
                    move_to_oven_batch["env"] = self.env
                    move_to_oven_batch["sim_time"] = self.bakery_state._sim_time
                    move_to_oven_batch["bakery_state"] = self.bakery_state
                    move_to_oven_batch["equipment"] = equipment
                    move_to_oven_batch["baker"] = baker
                    move_to_oven_batch["recipe"] = recipe
                    move_to_oven_batch["equipment_store"] = self.equipment_store
                    move_to_oven_batch["baker_store"] = self.baker_store
                    move_to_oven_batch["dependency"] = dependency
                    move_to_oven_batch["task_oven"] = task_oven

        
                    self.env.process(self.bakery_sim.move_to_oven(move_to_oven_batch))

                    self.env.run(until=yield_time + self.env.now)
                    self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
                    self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
                    self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
                    self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
                    self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
                    self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
                    self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
                    self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()
                    print('yield_time =',yield_time)
                    print('env =', self.env.now)

                    print('\ntime:', self.env.now)
                    print('time remaining:', self.bakery_state._sim_time)
                    self.bakery_state.print_dessert_case()
                    self.bakery_state.print_bakers()
                    self.bakery_state.print_equipment()
                    masking_array = self.set_game_masking()

                    action_array = self.map_masking_to_action(masking_array)

                    return self.bonsai_get_sim_state(masking_array,action_array)
                else:
                    self.env.run(until=yield_time + self.env.now)
                    self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
                    self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
                    self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
                    self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
                    self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
                    self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
                    self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
                    self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()
                    print('CAN NOT COMPLETE ACTION; NO VALUES IN MIXER; TRY AGAIN')
                    print('yield_time =',yield_time)
                    print('env =', self.env.now)
                    print('\ntime:', self.env.now)
                    print('time remaining:', self.bakery_state._sim_time)
                    masking_array = self.set_game_masking()

                    action_array = self.map_masking_to_action(masking_array)

                    return self.bonsai_get_sim_state(masking_array,action_array)
            else:
                masking_array = self.set_game_masking()

                action_array = self.map_masking_to_action(masking_array)

                return self.bonsai_get_sim_state(masking_array,action_array)

        elif action_string == "Chip_decorate_from_Oven_1" or action_string == "Chip_decorate_from_Oven_2" or action_string == "Chip_decorate_from_Oven_3" or action_string == "Eclair_decorate_from_Oven_1" or action_string == "Eclair_decorate_from_Oven_2" or action_string == "Eclair_decorate_from_Oven_3" or action_string == "Reese_decorate_from_Oven_1" or action_string == "Reese_decorate_from_Oven_2" or action_string == "Reese_decorate_from_Oven_3":
            if self.bakery_state.oven_1.current_recipe.name != RecipeNames.none or self.bakery_state.oven_2.current_recipe.name != RecipeNames.none  or self.bakery_state.oven_3.current_recipe.name != RecipeNames.none:

                if action_string == "Chip_decorate_from_Oven_1":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_1,1,3)

                if action_string == "Chip_decorate_from_Oven_2":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_2,1,4)

                if action_string == "Chip_decorate_from_Oven_3":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_3,1,5)

                if action_string == "Eclair_decorate_from_Oven_1":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_1,3,3)

                if action_string == "Eclair_decorate_from_Oven_2":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_2,3,4)

                if action_string == "Eclair_decorate_from_Oven_3":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_3,3,5)
                
                if action_string == "Reese_decorate_from_Oven_1":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_1,4,3)
            
                if action_string == "Reese_decorate_from_Oven_2":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_2,4,4)

                if action_string == "Reese_decorate_from_Oven_3":
                    recipe_baker_and_dependency = self.set_recipe_baker_and_dependency(EquipmentNames.oven_3,4,5)

                if (self.bakery_state.decorating_station_1.current_recipe.name == RecipeNames.none or self.bakery_state.decorating_station_1.current_recipe.name.value == 0): 
                    equipment = 6
                    
                elif (self.bakery_state.decorating_station_2.current_recipe.name == RecipeNames.none or self.bakery_state.decorating_station_2.current_recipe.name.value == 0):
                    equipment = 7

                else:
                    equipment = 0 #Waiting  

                baker = recipe_baker_and_dependency["baker"] #= baker
                recipe = recipe_baker_and_dependency["recipe"].name.value
                dependency = recipe_baker_and_dependency["dependency"] #= dependency

                task_decorate = Task('decoration',baker,equipment,dependency)

                move_to_decoration_station = {}
                move_to_decoration_station["env"] = self.env
                move_to_decoration_station["_sim_time"] = self.bakery_state._sim_time
                move_to_decoration_station["bakery_state"] = self.bakery_state
                move_to_decoration_station["equipment"] = equipment
                move_to_decoration_station["baker"] = baker
                move_to_decoration_station["recipe"] = recipe
                move_to_decoration_station["equipment_store"] = self.equipment_store
                move_to_decoration_station["baker_store"] = self.baker_store
                move_to_decoration_station["dependency"] = dependency
                move_to_decoration_station["task_decorate"] = task_decorate

    
                self.env.process(self.bakery_sim.move_to_decoration_station(move_to_decoration_station))

                self.env.run(until=yield_time + self.env.now)
                self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
                self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
                self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
                self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
                self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
                self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
                self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
                self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()
                print('\ntime:', self.env.now)
                print('time remaining:', self.bakery_state._sim_time)
                print('yield_time =',yield_time)
                print('env =', self.env.now)
                self.bakery_state.print_dessert_case()
                self.bakery_state.print_bakers()
                self.bakery_state.print_equipment()
                masking_array = self.set_game_masking()

                action_array = self.map_masking_to_action(masking_array)

                return self.bonsai_get_sim_state(masking_array,action_array)
            else:
                self.env.run(until=yield_time + self.env.now)
                self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
                self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
                self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
                self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
                self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
                self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
                self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
                self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()
                print('CAN NOT COMPLETE ACTION; NO VALUES IN MIXER; TRY AGAIN')
                print('yield_time =',yield_time)
                print('env =', self.env.now)
                print('\ntime:', self.env.now)
                print('time remaining:', self.bakery_state._sim_time)
                masking_array = self.set_game_masking()

                action_array = self.map_masking_to_action(masking_array)

                return self.bonsai_get_sim_state(masking_array,action_array)

        else:
            self.env.run(until=yield_time + self.env.now)
            self.bakery_state._sim_time = self.bakery_state._sim_time - yield_time
            self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
            self.bakery_state.mixer_1.time_remaining = self.bakery_state.mixer_1.set_remaining_time()
            self.bakery_state.mixer_2.time_remaining = self.bakery_state.mixer_2.set_remaining_time()
            self.bakery_state.oven_1.time_remaining = self.bakery_state.oven_1.set_remaining_time()
            self.bakery_state.oven_2.time_remaining = self.bakery_state.oven_2.set_remaining_time()
            self.bakery_state.oven_3.time_remaining = self.bakery_state.oven_3.set_remaining_time()
            self.bakery_state.decorating_station_1.time_remaining = self.bakery_state.decorating_station_1.set_remaining_time()
            self.bakery_state.decorating_station_2.time_remaining = self.bakery_state.decorating_station_2.set_remaining_time()
            print('CAN NOT COMPLETE ACTION; NO VALUES IN MIXER; TRY AGAIN')
            print('yield_time =',yield_time)
            print('env =', self.env.now)
            print('\ntime:', self.env.now)
            print('time remaining:', self.bakery_state._sim_time)
            masking_array = self.set_game_masking()

            action_array = self.map_masking_to_action(masking_array)

            return self.bonsai_get_sim_state(masking_array,action_array)


        return self.model.value_function()

    