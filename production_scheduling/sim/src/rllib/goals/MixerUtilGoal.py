from rllib.machine_teaching.goals import Goal


class MixerUtilGoal(Goal):
    mixer_in_use = 0

    def reward_fn(step_state,cookie_price,cupcake_price,cake_price) -> float:
        if (step_state['mixer_1_time_remaining'] == 0 and step_state['mixer_2_time_remaining'] == 0):
            return -1
        else:
            return 100

    def terminate_fn(self,mixers) -> bool:
        if (mixers/480) < 0.7:
            return True
        else:
            return False

    def step_metric(self,worker) -> float:
        #Storing values for evaluation 
        if worker.env.current_state["mixer_1_recipe"] != 0:
            self.mixer_in_use += 1
        elif worker.env.current_state["mixer_2_recipe"] != 0:
            self.mixer_in_use += 1
        else:
            self.mixer_in_use += 0

        return self.mixer_in_use

    def episode_success(self,mixers) -> bool:
        if (mixers/480) > 0.9:
            return True
        else:
            return False