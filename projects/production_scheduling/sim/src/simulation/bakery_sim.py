from typing import Dict, Any
import simpy
from .equipment import EquipmentNames
from .recipe import RecipeNames
from .baker import BakerNames
from .state import State
from .task import Task

yield_time = 1

class BakerySim:
    
    def reset(self, config, state) -> Dict[str, Any]:
        state.set_state(config)
        return state.get_state()
    
    def move_to_mixer(self,move_to_mixer_batch) -> Dict[str, Any]:
        yield_time = 1
        valid_task = False

        if len(move_to_mixer_batch["equipment_store"].items) > 0 and len(move_to_mixer_batch["baker_store"].items) > 0 and not valid_task:

            while not valid_task:

                if move_to_mixer_batch["task_mixer"].validate_task(move_to_mixer_batch):
                    if move_to_mixer_batch["baker"] == 0 and move_to_mixer_batch["equipment"]  == 0:
                        valid_task = True
                        return True

                    else:
                        valid_task = True

                        move_to_mixer_batch["env"].process(move_to_mixer_batch["task_mixer"].equipment_task(move_to_mixer_batch))
                        move_to_mixer_batch["env"].process(move_to_mixer_batch["task_mixer"].baker_task(move_to_mixer_batch))


                else:
                    break

        yield move_to_mixer_batch["env"].timeout(yield_time)

    def move_to_oven(self,move_to_oven_batch) -> Dict[str, Any]:
        yield_time = 1
        valid_task = False
        if move_to_oven_batch["equipment"] != 0:
            if len(move_to_oven_batch["equipment_store"].items) > 0 and len(move_to_oven_batch["baker_store"].items) > 0 and not valid_task:

                while not valid_task:

                    if move_to_oven_batch["task_oven"].validate_task(move_to_oven_batch):
                        
                        if move_to_oven_batch["baker"] == 0 and move_to_oven_batch["equipment"] == 0:
                            valid_task = True
                            return True

                        else:
                            valid_task = True
                            move_to_oven_batch["env"].process(move_to_oven_batch["task_oven"].equipment_task(move_to_oven_batch))
                            move_to_oven_batch["env"].process(move_to_oven_batch["task_oven"].baker_task(move_to_oven_batch))


                    else:
                        break

        yield move_to_oven_batch["env"].timeout(yield_time)

    def move_to_decoration_station(self,move_to_decoration_station) -> Dict[str, Any]:

        yield_time = 1
        valid_task = False
        if move_to_decoration_station["equipment"] != 0:
            if len(move_to_decoration_station["equipment_store"].items) > 0 and len(move_to_decoration_station["baker_store"].items) > 0 and not valid_task:

                while not valid_task:

                    if move_to_decoration_station["task_decorate"].validate_task(move_to_decoration_station):
                        
                        if move_to_decoration_station["baker"] == 0 and move_to_decoration_station["equipment"] == 0:
                            valid_task = True
                            return True

                        else:
                            valid_task = True
                            move_to_decoration_station["env"].process(move_to_decoration_station["task_decorate"].equipment_task(move_to_decoration_station))
                            move_to_decoration_station["env"].process(move_to_decoration_station["task_decorate"].baker_task(move_to_decoration_station))


                    else:
                        break

        yield move_to_decoration_station["env"].timeout(yield_time)





