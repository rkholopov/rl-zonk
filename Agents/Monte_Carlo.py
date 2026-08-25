import numpy as np
from Agents.Baseline import Baseline


class Monte_Carlo(Baseline):
    def __init__(self, soft):
        self.q = {}
        self.entries = {}
        self.soft = soft
        self.rng = np.random.default_rng()

    def action(self, state, pos_moves, optimal=False):
        self.q[state] = self.q.get(state, np.array([1500.0 for _ in range(pos_moves)]))
        if not(optimal) and self.soft != "Sampling" and self.rng.random() < self.soft:
            return self.rng.choice([i for i in range(pos_moves)])
        if not(optimal) and self.soft == "Sampling":
            return self.rng.choice([i for i in range(pos_moves)], p=self.softmax(self.q[state]))
        return int(np.argmax(self.q[state]))


    def update(self, episode):
        G = 0
        for s, a, r, s1, pos_moves in reversed(episode):
            G += r
            self.entries[s] = self.entries.get(s, [0 for _ in range(pos_moves)])
            self.entries[s][a] += 1
            self.q[s] = self.q.get(s, np.array([1500.0 for _ in range(pos_moves)]))
            self.q[s][a] += (G - self.q[s][a]) / self.entries[s][a]

    def softmax(self, x, t=50.0):
        shifted_x = x - np.max(x, axis=-1, keepdims=True)
        exp_x = np.exp(shifted_x) / t
        sum_exp_x = np.sum(exp_x, axis=-1, keepdims=True)
        return exp_x / sum_exp_x
