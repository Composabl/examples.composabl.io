from composabl import Teacher


class MinimizeCostTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        print(transformed_obs)
        return action

    def filtered_observation_space(self):
        return ["machines",
                "repairer_hourly_rate",
                "spare_cost",
                "machine_operating_hours",
                "downtime_cost_hourly_machine",
                "time_to_failure_min",
                "time_to_failure_max",
                "hours_to_repair_min",
                "hours_to_repair_max",
                "cost",
                "spares_level",
                ]

    def compute_reward(self, transformed_obs, action, sim_reward):
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        reward = 1 / (transformed_obs["cost"])
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 100

    def compute_termination(self, transformed_obs, action):
        return False
