import numpy as np


class Baseline:
    def __init__(self, soft, alpha, percentile):
        ...

    def action(self, state, pos_moves, optimal=False):
        if state[0] == "Stop/Continue":
            if state[1] == 6 and state[2] >= 16450:
                return 0
            elif state[1] == 5 and state[2] >= 3050:
                return 0
            elif state[1] == 4 and state[2] >= 1050:
                return 0
            elif state[1] == 3 and state[2] >= 400:
                return 0
            elif state[1] < 3 and state[2] >= 300:
                return 0
            elif state[2] < 300:
                return 0
            else:
                return 1
        else:
            return pos_moves-1

    def update(self, episode):
        ...

    def softmax(self, x, t=75.0):
        shifted_x = x - np.max(x, axis=-1, keepdims=True)
        exp_x = np.exp(shifted_x / t)
        sum_exp_x = np.sum(exp_x, axis=-1, keepdims=True)
        return exp_x / sum_exp_x