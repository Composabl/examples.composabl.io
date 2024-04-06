from rllib.machine_teaching.goals import Goal


import math


class RevenueUtilGoal(Goal):
    decoration_station_in_use = 0

    def reward_fn(step_state,cookie_price,cupcake_price,cake_price) -> float:
        reward = 0
        # print("Cookies",step_state['completed_cookies'])
        # print("Cookie Price",cookie_price)
        if (step_state['completed_cookies'] > 0 and cookie_price > 0):
            reward += math.log(step_state['completed_cookies']*cookie_price,2)
        if (step_state['completed_cupcakes'] > 0 and cupcake_price > 0):
            reward += math.log(step_state['completed_cupcakes']*cupcake_price,2)
        if (step_state['completed_cake'] > 0 and cake_price > 0):
            reward += math.log(step_state['completed_cake']*cake_price,2)

        return reward

    def terminate_fn(self) -> bool:
        if(self.completed_cookies == 0 and self.completed_cupcakes == 0 and self.completed_cake == 0):
            return True
        else:
            return False

    def step_metric(self,worker):
        #How to pass in the worker to evaluate
        if worker.env.current_state["decorating_station_1_recipe"] != 0:
            self.decoration_station_in_use += 1
        elif worker.env.current_state["decorating_station_2_recipe"] != 0:
            self.decoration_station_in_use += 1
        else:
            self.decoration_station_in_use += 0

        return self.decoration_station_in_use

    def episode_success(self,revenue_equip) -> bool:
        if ((revenue_equip/480) > 0.7):
            return True
        else:
            return False