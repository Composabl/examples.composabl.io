from composabl import Teacher


class DRLControlReactor(Teacher):
    def __init__(self, target_temperature=350):
        # Initialize necessary attributes or variables
        self.target_temperature = target_temperature

    def compute_reward(self, transformed_obs, action, sim_reward):
        # Get observed temperature
        current_temperature = transformed_obs["T"]

        # Reward based on proximity to the target temperature
        reward = 1 if abs(current_temperature - self.target_temperature) <= 5 else -1

        return reward

    def compute_action_mask(self, transformed_obs, action):
        # Placeholder logic for action masking (if needed)
        return None  # Allow all actions

    def compute_success_criteria(self, transformed_obs, action):
        # Placeholder logic for success criteria (if needed)
        return False  # Adjust based on success conditions

    def compute_termination(self, transformed_obs, action):
        # Placeholder logic for termination conditions (if needed)
        return False  # Termination condition based on specific criteria

    def transform_obs(self, obs, action):
        # Placeholder logic for observation transformation
        return obs

    def transform_action(self, transformed_obs, action):
        # Placeholder logic for action transformation (if needed)
        return action

    def filtered_observation_space(self):
        # Define the observation space used by this skill
        return ["T"]


class DRLStartReaction(Teacher):
    def __init__(self, temperature_threshold=320, concentration_threshold=0.1):
        # Initialize necessary attributes or variables
        self.temperature_threshold = (
            temperature_threshold  # Define temperature threshold for reaction start
        )
        self.concentration_threshold = (
            concentration_threshold  # Define concentration threshold for reaction start
        )
        self.reaction_started = False  # Flag to track reaction initiation

    def compute_reward(self, transformed_obs, action, sim_reward):
        return 0  # No specific reward in this context

    def compute_action_mask(self, transformed_obs, action):
        return None  # Allow all actions

    def compute_success_criteria(self, transformed_obs, action):
        return self.reaction_started  # Consider criteria based on reaction start

    def compute_termination(self, transformed_obs, action):
        return False  # Termination condition based on specific criteria

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return [
            "T",
            "Ca",
        ]

    def determine_reaction_start(self, obs):
        # Check if the reaction has started based on sensor observations
        current_temperature = obs.get("T", 0)  # Get current temperature
        current_concentration = obs.get("Ca", 0)  # Get current concentration

        # Check if temperature and concentration cross thresholds
        if (
            current_temperature >= self.temperature_threshold
            and current_concentration >= self.concentration_threshold
        ):
            self.reaction_started = True  # Set flag for reaction start

    def process_observation(self, obs):
        # Process incoming observations to determine reaction start
        self.determine_reaction_start(obs)


class DRLControlTransition(Teacher):
    def __init__(self, start_temperature=10, target_temperature=40):
        self.start_temperature = start_temperature
        self.target_temperature = target_temperature

    def compute_reward(self, transformed_obs, action, sim_reward):
        current_temperature = transformed_obs.get("T", 0)

        # Calculate the reward based on proximity to the target temperature range
        reward = 1 - abs(current_temperature - self.target_temperature) / (
            self.target_temperature - self.start_temperature
        )
        return max(0, reward)  # Ensure positive reward

    def compute_action_mask(self, transformed_obs, action):
        return None  # Allow all actions

    def compute_success_criteria(self, transformed_obs, action):
        return False  # Adjust based on success conditions

    def compute_termination(self, transformed_obs, action):
        return False  # Termination condition based on specific criteria

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["T"]  # Adjust based on your observation space


class DRLProduceProduct(Teacher):
    def __init__(self):
        self.total_product_produced = 0  # Track total product produced

    def compute_reward(self, transformed_obs, action, sim_reward):
        product_concentration = transformed_obs.get("Ca", 0)
        product_produced = product_concentration - self.total_product_produced
        self.total_product_produced = (
            product_concentration  # Update total product produced
        )
        return product_produced  # Reward based on product concentration change

    def compute_action_mask(self, transformed_obs, action):
        return None  # Allow all actions

    def compute_success_criteria(self, transformed_obs, action):
        return False  # Adjust based on success conditions

    def compute_termination(self, transformed_obs, action):
        return False  # Termination condition based on specific criteria

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["Ca"]  # Assuming "Ca" sensor measures product concentration


class DRLDetermineSetpoint(Teacher):
    def __init__(self):
        # Initialize necessary attributes or variables
        self.setpoint = 0  # Initial setpoint placeholder

    def compute_reward(self, transformed_obs, action, sim_reward):
        # Consider rewarding based on how close the setpoint is to the observed temperature
        current_temperature = transformed_obs.get("T", 0)  # Get observed temperature
        reward = (
            1 - abs(current_temperature - self.setpoint) / self.setpoint
        )  # Reward based on proximity
        return reward

    def compute_action_mask(self, transformed_obs, action):
        return None  # Allow all actions

    def compute_success_criteria(self, transformed_obs, action):
        return False  # Adjust based on success conditions

    def compute_termination(self, transformed_obs, action):
        return False  # Termination condition based on specific criteria

    def transform_obs(self, obs, action):
        return obs

    def transform_action(self, transformed_obs, action):
        return action

    def filtered_observation_space(self):
        return ["T"]
