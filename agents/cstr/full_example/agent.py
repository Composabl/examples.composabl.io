import os

from composabl import Agent, Runtime, Scenario, Sensor, Skill, Perceptor
from perceptors import PerceptorPredictThermalRunaway
from controllers import (
    ControllerSelectControlStrategy,
    ControllerControlReactor,
    ControllerControlToSetPoint,
    RockwellControlToSetPoint,
)
from teachers import (
    DRLControlReactor,
    DRLStartReaction,
    DRLControlTransition,
    DRLProduceProduct,
    DRLDetermineSetpoint,
)

license_key = os.environ["COMPOSABL_LICENSE"]

PATH = os.path.dirname(os.path.realpath(__file__))
PATH_HISTORY = f"{PATH}/history"
PATH_CHECKPOINTS = f"{PATH}/checkpoints"


def start():
    # ==========================================
    # Config
    # ==========================================
    config = {
        "license": license_key,
        "target": {"docker": {"image": "composabl/sim-cstr:latest"}},
        "env": {
            "name": "sim-cstr",
        },
        "runtime": {"workers": 1},
    }

    runtime = Runtime(config)
    a = Agent()

    # ==========================================
    # Sensors
    # ==========================================
    a.add_sensors(
        [
            # Measures the temperature inside the reactor vessel.
            Sensor("T", "Internal Reactor Temperature"),
            # Monitors the temperature of the cooling or heating jacket
            # surrounding the reactor vessel.
            Sensor("Tc", "Cooling/Heating Jacket Temperature"),
            # Measures the concentration of a specific component, denoted
            # as 'a', within the reactor.
            Sensor("Ca", "Component 'a' Concentration"),
            # Measures a reference concentration value.
            # Provides a reference point against which the actual
            # component concentrations are compared for control
            # or target purposes.
            Sensor("Cref", "Reference Concentration"),
            # Measures a reference temperature value.
            # Used as a target or setpoint for reactor temperature control
            Sensor("Tref", "Reference Temperature"),
        ]
    )

    # ==========================================
    # Perceptors
    # ==========================================
    a.add_perceptor(
        Perceptor(["thermal_runaway_predict"], PerceptorPredictThermalRunaway, "")
    )

    # ==========================================
    # Skills
    # ==========================================
    s_control_reactor = Skill("control_reactor", ControllerControlReactor)
    s_control_reactor_2 = Skill("control_reactor_2", DRLControlReactor)
    s_start_reaction = Skill("start_reaction", DRLStartReaction)
    s_control_transition = Skill("control_transition", DRLControlTransition)
    s_produce_product = Skill("produce_product", DRLProduceProduct)
    s_determine_setpoint = Skill("determine_setpoint", DRLDetermineSetpoint)
    s_control_to_setpoint = Skill("control_to_setpoint", ControllerControlToSetPoint)
    s_control_to_setpoint_2 = Skill("control_to_setpoint_2", RockwellControlToSetPoint)

    a.add_skill(s_control_reactor)
    a.add_skill(s_control_reactor_2)
    a.add_skill(s_start_reaction)
    a.add_skill(s_control_transition)
    a.add_skill(s_produce_product)
    a.add_skill(s_determine_setpoint)
    a.add_skill(s_control_to_setpoint)
    a.add_skill(s_control_to_setpoint_2)

    # ==========================================
    # Selectors
    # ==========================================
    s_select_control_strategy = Skill(
        "select_control_strategy", ControllerSelectControlStrategy
    )
    s_select_control_strategy.add_scenario(Scenario({"Cref_signal": "ss1"}))
    s_select_control_strategy.add_scenario(Scenario({"Cref_signal": "ss2"}))
    s_select_control_strategy.add_scenario(Scenario({"Cref_signal": "transition"}))
    s_select_control_strategy.add_scenario(Scenario({"Cref_signal": "complete"}))

    a.add_selector_skill(
        s_select_control_strategy,
        [
            s_control_reactor,
            s_control_reactor_2,
            s_start_reaction,
            s_control_transition,
            s_produce_product,
            s_determine_setpoint,
            s_control_to_setpoint,
            s_control_to_setpoint_2,
        ],
    )

    # ==========================================
    # Skills
    # ==========================================
    j = a.to_json()
    print(j)

    # runtime.train(agent)


if __name__ == "__main__":
    # start_pre()
    start()
    # start_post()
