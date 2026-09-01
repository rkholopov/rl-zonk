import numpy as np
from Agents.Monte_Carlo import MonteCarlo


class QLearning(MonteCarlo):
    def __init__(self, soft, alpha):
        super().__init__(soft)
        self.q = {}
        self.soft = soft
        self.alpha = alpha
        self.rng = np.random.default_rng()

    def update(self, episode):
        for s, a, r, s1, pos_moves in reversed(episode):
            self.q[s] = self.q.get(s, np.array([1500.0 for _ in range(pos_moves)]))
            if s1 not in self.q.keys():
                v = 0
            else:
                v = np.max(self.q[s1])
            self.q[s][a] += self.alpha * (r + v - self.q[s][a])
