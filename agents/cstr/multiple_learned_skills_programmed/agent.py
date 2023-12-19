import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from sensors import sensors
from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher
from composabl import Controller

license_key = os.environ["COMPOSABL_LICENSE"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"

class ProgrammedSelector(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if obs['Cref'] >= 8.56 and obs['Cref'] <= 8.58:
            action = [0]
        elif obs['Cref'] == 2.0:
            action = [1]
        else:
            action = [2]

        return action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_success_criteria(self, transformed_obs, action):
        return False

    def compute_termination(self, transformed_obs, action):
        return False



def start():
    # delete old history files
    try:
        files = os.listdir(PATH_HISTORY)

        pkl_files = [file for file in files if file.endswith('.pkl')]
        for file in pkl_files:
            file_path = os.path.join(dir, file)
            os.remove(file_path)
    except:
        pass

    # Cref_signal is a configuration variable for Concentration and Temperature setpoints
    ss1_scenarios = [
        {
            "Cref_signal": "ss1"
        }
    ]

    ss2_scenarios = [
        {
            "Cref_signal": "ss2"
        }
    ]

    transition_scenarios = [
        {
            "Cref_signal": "transition"
        }
    ]

    selector_scenarios = [
        {
            "Cref_signal": "complete"
        }
    ]

    ss1_skill = Skill("ss1", SS1Teacher)
    for scenario_dict in ss1_scenarios:
        ss1_skill.add_scenario(Scenario(scenario_dict))

    ss2_skill = Skill("ss2", SS2Teacher)
    for scenario_dict in ss2_scenarios:
        ss2_skill.add_scenario(Scenario(scenario_dict))

    transition_skill = Skill("transition", TransitionTeacher)
    for scenario_dict in transition_scenarios:
        transition_skill.add_scenario(Scenario(scenario_dict))

    selector_skill = Skill("selector", ProgrammedSelector)
    for scenario_dict in selector_scenarios:
        selector_skill.add_scenario(Scenario(scenario_dict))

    config = {
        "license": license_key,
        "target": {
            "docker": {
                "image": "composabl/sim-cstr:latest"
            },
            #"local": {
            #    "address": "localhost:1337"
            #}
        },
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {
            "ray": {
                "workers": 1
            }
        }
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss2_skill, transition_skill, ss1_skill], fixed_order=False, fixed_order_repeat=False)

    try:
        files = os.listdir(PATH_CHECKPOINTS)

        if '.DS_Store' in files:
            files.remove('.DS_Store')
            os.remove(PATH_CHECKPOINTS + '/.DS_Store')

        if len(files) > 0:
            agent.load(PATH_CHECKPOINTS)

    except Exception:
        os.mkdir(PATH_CHECKPOINTS)

    # train agent
    runtime.train(agent, train_iters=200)

    # save agent
    agent.export(PATH_CHECKPOINTS)


if __name__ == "__main__":
    start()
