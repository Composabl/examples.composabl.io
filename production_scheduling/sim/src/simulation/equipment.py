import simpy
from enum import Enum
from .recipe import Recipe, RecipeNames

class EquipmentNames(Enum):
    none = 0
    mixer_1= 1
    mixer_2= 2
    oven_1 = 3
    oven_2 = 4
    oven_3 = 5
    decorating_station_1= 6
    decorating_station_2= 7

class Equipment:

    def __init__(self, name : str, environment : simpy.Environment):
        self.name = name
        self.current_recipe : Recipe = Recipe(RecipeNames.none,0,0,0,0)
        self._start_time : int = None
        self._environment = environment
        self.time_remaining : int = 0

    def set_remaining_time(self) -> int: 

        if self._start_time != None:
            set_time_remaining = self._finish_time() - self._environment.now
            if set_time_remaining > 0:
                return set_time_remaining
            else: 
                return 0
        else:
            return 0

        #return self.time_remaining 

    def _finish_time(self) -> int:
        equipment_group = ''
        if self.current_recipe == RecipeNames.none:
            return 0
        if self.name == EquipmentNames.mixer_1.name or self.name == EquipmentNames.mixer_2.name:  #if self.name == 'mixer_1' or self.name == 'mixer_2':
            equipment_group = 'mixer'
        if self.name == EquipmentNames.oven_1.name or self.name == EquipmentNames.oven_2.name or self.name == EquipmentNames.oven_3.name:  #if self.name == 'oven_1' or self.name == 'oven_2' or self.name == 'oven_3':
            equipment_group = 'oven'
        if self.name == EquipmentNames.decorating_station_1.name or self.name == EquipmentNames.decorating_station_2.name: #if self.name == 'decorating_station_1' or self.name == 'decorating_station_2':
            equipment_group = 'decorating_station'
                    
        return self._start_time + self.current_recipe.times[equipment_group]

    def set_in_use(self, recipe : Recipe, start_time : int, task_time:int) -> None:
        self.current_recipe = recipe
        self._start_time = start_time
        self.time_remaining = task_time

    def set_not_in_use(self) -> None:
        self.current_recipe = Recipe(RecipeNames.none,0,0,0,0)
        self._start_time = None

    def print_equipment(self) -> None:

        if self.current_recipe == None:
            print(self.name + ':', '-')

        elif self.time_remaining == 0:
            print(self.name + ':', self.current_recipe.name, 'ready!')

        else:
            print(self.name + ':', self.current_recipe.name, 'in', self.time_remaining, 'mins left') 

    def print_game_equipment(self) -> None:

        if self.current_recipe == None:
            print(self.name + ':', '-')

        elif self.time_remaining == 0:
            print(self.name + ':', self.current_recipe.name, 'ready!')

        else:
            print(self.name + ':', self.current_recipe.name, 'in', self.time_remaining, 'mins left') 
