import string
import simpy
from .equipment import Equipment, EquipmentNames
from .recipe import Recipe, RecipeNames
from .baker import Baker, BakerNames
from .state import State

DEFAULT_SUGAR = 1
DEFAULT_BUTTER = 1
DEFAULT_EGGS = 1
DEFAULT_FLOUR = 1
DEFAULT_BAKING_SODA = 1
DEFAULT_MILK = 1

class Task:

    def __init__(
        self,
        type : string,
        baker : int,
        equipment : int,
        dependency : int
    ):
        self.type = type,
        self.baker = baker,
        self.equipment = equipment,
        self.dependency = dependency
        
    def equipment_task(self, task_data) -> None :
        recipe : Recipe = task_data["bakery_state"].recipes[RecipeNames(task_data["recipe"])]
        equipment_name = EquipmentNames(task_data["equipment"]).name

        equipment_group = ''

        if equipment_name == EquipmentNames.mixer_1.name or equipment_name == EquipmentNames.mixer_2.name:
            equipment_group = 'mixer'
        elif equipment_name == EquipmentNames.oven_1.name or equipment_name == EquipmentNames.oven_2.name or equipment_name == EquipmentNames.oven_3.name:
            equipment_group = 'oven'
        elif  equipment_name == EquipmentNames.decorating_station_1.name or equipment_name== EquipmentNames.decorating_station_2.name:
            equipment_group = 'decorating_station'

        if equipment_name == EquipmentNames.mixer_1.name or equipment_name == EquipmentNames.mixer_2.name:

            to_equipment : Equipment = yield task_data["equipment_store"].get(lambda x: x.name == equipment_name)

            to_equipment.set_in_use(recipe, task_data["env"].now,recipe.times[equipment_group])

        if equipment_name == EquipmentNames.oven_1.name or equipment_name == EquipmentNames.oven_2.name or equipment_name == EquipmentNames.oven_3.name:
            from_equipment : Equipment = yield task_data["equipment_store"].get(lambda x: x.name == EquipmentNames(task_data["dependency"]).name)
            from_equipment.set_not_in_use()
            yield task_data["equipment_store"].put(from_equipment)

            to_equipment : Equipment = yield task_data["equipment_store"].get(lambda x: x.name == equipment_name)

            to_equipment.set_in_use(recipe, task_data["env"].now, recipe.times[equipment_group])

        if equipment_name == EquipmentNames.decorating_station_1.name or equipment_name == EquipmentNames.decorating_station_2.name:
            from_equipment : Equipment = yield task_data["equipment_store"].get(lambda x: x.name == EquipmentNames(task_data["dependency"]).name)
            from_equipment.set_not_in_use()
            yield task_data["equipment_store"].put(from_equipment)

            to_equipment : Equipment = yield task_data["equipment_store"].get(lambda x: x.name == equipment_name)

            to_equipment.set_in_use(recipe, task_data["env"].now, recipe.times[equipment_group])
        
        yield task_data["env"].timeout(recipe.times[equipment_group])

        yield task_data["equipment_store"].put(to_equipment)

    def baker_task(self, task_data) -> int:
        recipe : Recipe = task_data["bakery_state"].recipes[RecipeNames(task_data["recipe"])]
        baker : Baker = yield task_data["baker_store"].get(lambda x: x.name == BakerNames(task_data["baker"]))
        task_time = None

        equipment_group = ''
        if EquipmentNames(task_data["equipment"]).name == EquipmentNames.mixer_1.name or EquipmentNames(task_data["equipment"]).name == EquipmentNames.mixer_2.name:
            equipment_group = 'mixer'
        if EquipmentNames(task_data["equipment"]).name == EquipmentNames.oven_1.name or EquipmentNames(task_data["equipment"]).name == EquipmentNames.oven_2.name or EquipmentNames(task_data["equipment"]).name == EquipmentNames.oven_3.name:
            equipment_group = 'oven'
        if  EquipmentNames(task_data["equipment"]).name == EquipmentNames.decorating_station_1.name or EquipmentNames(task_data["equipment"]).name== EquipmentNames.decorating_station_2.name:
            equipment_group = 'decorating_station'
            
        task_time = recipe.times[equipment_group]

        baker.set_as_busy(task_time)

        yield task_data["env"].timeout(task_time)

        baker.set_as_not_busy()

        yield task_data["baker_store"].put(baker)
        return task_time

    def validate_task(self, task_data) -> bool:
        recipe : Recipe = task_data["bakery_state"].recipes[RecipeNames(task_data["recipe"])]
        baker : Baker = yield task_data["baker_store"].get(lambda x: x.name == BakerNames(task_data["baker"]))

        equipment_group = ''
        if EquipmentNames(task_data["equipment"]).name == EquipmentNames.mixer_1.name or EquipmentNames(task_data["equipment"]).name == EquipmentNames.mixer_2.name:
            equipment_group = 'mixer'
        if EquipmentNames(task_data["equipment"]).name == EquipmentNames.oven_1.name or EquipmentNames(task_data["equipment"]).name == EquipmentNames.oven_2.name or EquipmentNames(task_data["equipment"]).name == EquipmentNames.oven_3.name:
            equipment_group = 'oven'
        if  EquipmentNames(task_data["equipment"]).name == EquipmentNames.decorating_station_1.name or EquipmentNames(task_data["equipment"]).name== EquipmentNames.decorating_station_2.name:
            equipment_group = 'decorating_station'
            
        task_time = recipe.times[equipment_group]

        if RecipeNames(task_data["recipe"]) == RecipeNames.none:
            return False
            
        if task_data["baker"] == 0 and task_data["equipment"] == 0:
            return True

        available_bakers = [x for x in task_data["baker_store"].items if x.name == BakerNames(task_data["baker"]) and (x.busy_for == 0 or x.busy_for == None) and baker.can_complete_task(EquipmentNames(task_data["equipment"]).name,recipe,task_time)] 

        available_equipment = [x for x in task_data["equipment_store"].items if x.name == EquipmentNames(task_data["equipment"]).name and (x.current_recipe == RecipeNames.none or x.current_recipe == None)] 

        return len(available_bakers) > 0 and len(available_equipment) > 0 