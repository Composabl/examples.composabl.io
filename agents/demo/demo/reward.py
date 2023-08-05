import math


class RewardStabilize:
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def __call__(self, obs):
        if self.obs_history is None:
            self.obs_history = [obs]
            return 0

        reward = 0

        if abs(self.obs_history[-1][4]) >= abs(obs[4]) + 0.1 * 180 / math.pi:
            reward += 1

        # has the x position remained stable?
        if abs(self.obs_history[-1][0] - obs[0]) <= self.error_tolerance * (
            self.width / self.scale / 2
        ):
            reward += 1
        else:
            reward -= 1

        # has the y position remained stable?
        if abs(self.obs_history[-1][1] - obs[1]) <= self.error_tolerance * (
            self.width / self.scale / 2
        ):
            reward += 1
        else:
            reward -= 1

        self.obs_history.append(obs)
        return reward


class RewardMoveToCenter:
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def __call__(self, obs):
        if self.obs_history is None:
            self.obs_history = [obs]
            return 0

        VIEWPORT_W = 600
        VIEWPORT_H = 400
        SCALE = 30.0

        reward = 0

        # if in the center, give a reward
        if abs(obs[0]) < 0.1:
            reward += 0.5
        else:
            # has the x position moved closer to the center (0)?
            if abs(self.obs_history[-1][0]) - abs(obs[0]) > 0:
                reward += 1
            else:
                reward -= 1

        # has the y position remained stable?
        if (self.obs_history[-1][1] - obs[1]) * (VIEWPORT_W / SCALE / 2) < 0.1:
            reward += 1
        else:
            reward -= 1

        # are we level?
        if abs(obs[4]) * 180 / math.pi < 5:
            reward += 1
        else:
            reward -= 1

        self.obs_history.append(obs)
        return reward


class RewardLand:
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def __call__(self, obs):
        if self.obs_history is None:
            self.obs_history = [obs]
            return 0

        VIEWPORT_W = 600
        VIEWPORT_H = 400
        SCALE = 30.0

        reward = 0

        # has the y position moved closer to the center (0)?
        if abs(self.obs_history[-1][1]) >= abs(obs[0]) + 0.1 * 180 / math.pi:
            reward += 1
        else:
            reward -= 1

        # has the angle remained stable?
        if abs(self.obs_history[-1][4] - obs[4]) <= 0.01 * (VIEWPORT_W / SCALE / 2):
            reward += 1

        # has the x position remained stable?
        if abs(self.obs_history[-1][0] - obs[0]) <= 0.01 * (VIEWPORT_W / SCALE / 2):
            reward += 1
        else:
            reward -= 1

        if abs(self.obs_history[-1][1]) - abs(obs[1]) >= 0.1 * 180 / math.pi:
            reward -= 2

        # have we landed?
        if obs[-1] and obs[-2]:
            reward += 1000

        self.obs_history.append(obs)
        return reward


# sparse reward structure
class RewardSelector:
    def __init__(self):
        self.obs_history = None
        self.width = 600
        self.scale = 30
        self.error_tolerance = 0.01

    def __call__(self, obs):
        if self.obs_history is None:
            self.obs_history = [obs]
            return 0

        reward = 0

        # landed
        if obs[-1] and obs[-2]:
            # in the goal!
            if abs(obs[0]) < 0.15:
                reward += 100
        elif abs(obs[0]) < 0.15:
            reward += 1

        # has the y position moved closer to the center (0)?
        if abs(self.obs_history[-1][1]) >= abs(obs[0]) + 0.1 * 180 / math.pi:
            reward += 1
        else:
            reward -= 1

        self.obs_history.append(obs)
        return reward
