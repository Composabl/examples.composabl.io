from rllib.machine_teaching.goals import Goal


class DecorationStationUtilGoal(Goal):
    decoration_station_in_use = 0

    def reward_fn(step_state,cookie_price,cupcake_price,cake_price) -> float:
        if(step_state['decorating_station_1_time_remaining'] == 0 and step_state['decorating_station_2_time_remaining']  == 0):
            return -1
        else:
            return 100

    def terminate_fn(self) -> bool:
        if(self.decorating_station_1_recipe == 0 and self.decorating_station_2_recipe == 0):
            return True
        else:
            return False

    def step_metric(self,worker) -> float:
        #How to pass in the worker to evaluate 
        if worker.env.current_state["decorating_station_1_recipe"] != 0:
            self.decoration_station_in_use += 1
        elif worker.env.current_state["decorating_station_2_recipe"] != 0:
            self.decoration_station_in_use += 1
        else:
            self.decoration_station_in_use += 0
        return self.decoration_station_in_use

    def episode_success(self,decoration_stations) -> bool:
        #If successful with mixing and decorating, revenue reward 
        if (decoration_stations/480) > 0.9:
            return True
        else:
            return False