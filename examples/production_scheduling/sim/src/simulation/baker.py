import simpy
from .equipment import EquipmentNames
from .recipe import Recipe
from enum import Enum

class BakerNames(Enum):
    Chip = 1
    Coco = 2 
    Eclair = 3
    Reese = 4
    
class Baker:

    def __init__(self, env : simpy.Environment, sim_time : int, name : BakerNames, trained_on_mixer : bool, trained_on_oven : bool, trained_on_decorating : bool, shift_from : int, shift_to : int):

        self.name = name

        self.trained_on = {
            EquipmentNames.mixer_1 : trained_on_mixer,
            EquipmentNames.mixer_2 : trained_on_mixer,
            EquipmentNames.oven_1 : trained_on_oven,
            EquipmentNames.oven_2 : trained_on_oven,
            EquipmentNames.oven_3 : trained_on_oven,
            EquipmentNames.decorating_station_1 : trained_on_decorating,
            EquipmentNames.decorating_station_2 : trained_on_decorating
        }

        self._environment = env
        self._sim_time = sim_time
        self.shift_from = shift_from
        self.shift_to = shift_to
        self.busy_for = 0
        self._start_time: int = None

    def remaining_time(self) -> int: 
        if self._start_time != None:
            set_time_remaining = (self._start_time + self.busy_for) - self._environment.now
            if set_time_remaining > 0:
                return set_time_remaining
            else: 
                return 0
        else:
            return 0
    def set_as_busy(self, task_time : int) -> None:
        self._start_time = self._environment.now
        self.busy_for = task_time

    def set_as_not_busy(self) -> None:
        self._start_time = None
        self.busy_for = 0

    def can_complete_task(self, equipment : EquipmentNames, recipe : Recipe, task_time) -> bool:
        
        if self._environment.now >= self.shift_from and self._environment.now + task_time <= self.shift_to and self.busy_for == None and self.trained_on[equipment]:
            return True
        else:
            return False

    def print_baker(self) -> None:
        print(self.name.name, 'is trained on:', 
            EquipmentNames.mixer_1.name if self.trained_on[EquipmentNames.mixer_1] else '-',
            EquipmentNames.mixer_2.name if self.trained_on[EquipmentNames.mixer_2] else '-',
            EquipmentNames.oven_1.name if self.trained_on[EquipmentNames.oven_1] else '-',
            EquipmentNames.oven_2.name if self.trained_on[EquipmentNames.oven_2] else '-',
            EquipmentNames.oven_3.name if self.trained_on[EquipmentNames.oven_3] else '-',
            EquipmentNames.decorating_station_1.name if self.trained_on[EquipmentNames.decorating_station_1] else '-',
            EquipmentNames.decorating_station_2.name if self.trained_on[EquipmentNames.decorating_station_2] else '-',
        )
        if self._environment.now < self.shift_from:
            print(' - arriving in', self.shift_from - self._environment.now, 'mins')
        elif self.busy_for != 0 and self.busy_for != None:
            print(' - busy for', self.busy_for - self._environment.now, 'mins')
        else:
            print(' - ready!')

        if self.shift_to < self._sim_time and self.shift_to > self._environment.now:
            print(' - leaving in', self.shift_to - self._environment.now, 'mins')

        