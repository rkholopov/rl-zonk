import numpy as np


class Baseline:
    def __init__(self, soft, alpha, percentile):
        ...

    def action(self, state, pos_moves, optimal=False):
        phase, score, num_dice = state[:3]
        if phase == 2:
            raise ValueError("No actions in a terminal state")
        if phase == 1:
            return pos_moves - 1
        if score < 300:
            return 0
        thresholds = {1: 300, 2: 300, 3: 400, 4: 1050, 5: 3050, 6: 16450}
        return 0 if score >= thresholds[num_dice] else 1

    def update(self, episode):
        ...

    def softmax(self, x, t=75.0):
        shifted_x = x - np.max(x, axis=-1, keepdims=True)
        exp_x = np.exp(shifted_x / t)
        sum_exp_x = np.sum(exp_x, axis=-1, keepdims=True)
        return exp_x / sum_exp_x