from composabl.ray import Runtime

# from composabl.core import Agent, Skill, Sensor, Scenario, Teacher

from composabl import Agent, Skill, Sensor, Scenario, Teacher

# from composabl.core.agent import Teacher


class ReachTeacher(Teacher):
    def __init__(self):
        self.obs_history = None
        self.reward_history = []
        self.last_reward = 0

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["state1", "time_counter"]

    def compute_reward(self, transformed_obs, action):
        print(transformed_obs)
        if self.obs_history is None:
            self.obs_history = [transformed_obs]
            return 0
        else:
            self.obs_history.append(transformed_obs)

        reward = transformed_obs[0]
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None

    def compute_success_criteria(self, transformed_obs, action):
        return len(self.obs_history) > 1000

    def compute_termination(self, transformed_obs, action):
        return False


# LICENSE_KEY = os.environ.get("LICENSE_KEY", None)


def start():
    # Observation Space
    # The state is an 8-dimensional vector: the coordinates of the lander in `x` & `y`, its linear

    state1 = Sensor("state1", "dummy variable that accumulates an action value")
    time_counter = Sensor("time_counter", "")

    sensors = [state1, time_counter]

    reach_scenarios = [
        {state1: 0, time_counter: 0},
        {state1: -100, time_counter: 0},
        {state1: 100, time_counter: 0},
    ]

    reach_skill = Skill("reach", ReachTeacher, trainable=True)
    for scenario_dict in reach_scenarios:
        scenario = Scenario(scenario_dict)
        reach_skill.add_scenario(scenario)

    config = {
        "env": {
            "name": "my_simulator",
            "compute": "local",  # "docker", "kubernetes", "local"
            "config": {
                "address": "localhost:1337",
                # "use_gpu": False,  # @todo: doesn't do anything yet
                # "image": "composabl/sim-lunar-lander:latest"
            },
        },
        "license": "",
        "training": {},
    }
    runtime = Runtime(config)
    agent = Agent(runtime, config)
    agent.add_sensors(sensors)

    agent.add_skill(reach_skill)
    # agent.add_selector_skill(selector_skill, [stabilize_skill, move_to_center_skill, land_skill], fixed_order=True, repeat=False)
    agent.train(train_iters=5)
