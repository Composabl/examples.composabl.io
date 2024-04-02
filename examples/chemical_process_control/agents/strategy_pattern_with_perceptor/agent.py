import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill
from perceptors import perceptors

from teacher import CSTRTeacher, SS1Teacher, SS2Teacher, TransitionTeacher

license_key = os.environ["COMPOSABL_LICENSE"]

from composabl import Controller

class ProgrammedSelector(Controller):
    def __init__(self):
        self.counter = 0

    def compute_action(self, obs):
        if self.counter < 22:
            action = [0]
        elif self.counter < 74 : #transition
            action = [1]
        else:
            action = [2]

        self.counter += 1

        return action

    def transform_obs(self, obs):
        return obs

    def filtered_observation_space(self):
        return ['T', 'Tc', 'Ca', 'Cref', 'Tref']

    def compute_success_criteria(self, transformed_obs, action):
        if self.counter > 100:
            return True

    def compute_termination(self, transformed_obs, action):
        return False



def start():
    # delete old history files
    dir = './cstr/multiple_skills_perceptor'
    files = os.listdir(dir)
    pkl_files = [file for file in files if file.endswith('.pkl')]
    for file in pkl_files:
        file_path = os.path.join(dir, file)
        os.remove(file_path)

    T = Sensor("T", "")
    Tc = Sensor("Tc", "")
    Ca = Sensor("Ca", "")
    Cref = Sensor("Cref", "")
    Tref = Sensor("Tref", "")

    sensors = [T, Tc, Ca, Cref, Tref]

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
                "workers": 4
            }
        },

        "flags": {
            "print_debug_info": True
        }
    }

    runtime = Runtime(config)
    agent = Agent()
    agent.add_sensors(sensors)
    agent.add_perceptors(perceptors)

    agent.add_skill(ss1_skill)
    agent.add_skill(ss2_skill)
    agent.add_skill(transition_skill)
    agent.add_selector_skill(selector_skill, [ss1_skill, transition_skill, ss2_skill], fixed_order=False, fixed_order_repeat=False)

    checkpoint_path = './cstr/multiple_skills_perceptor/saved_agents/'

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
    runtime.train(agent, train_iters=10)

    # save agent
    agent.export(checkpoint_path)


if __name__ == "__main__":
    start()
