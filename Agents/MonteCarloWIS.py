import numpy as np
from Agents.Monte_Carlo import MonteCarlo


class MonteCarloWIS(MonteCarlo):
    def __init__(self, soft, alpha, percentile):
        super().__init__(soft, alpha, percentile)
        self.q = {}
        self.weights = {}
        self.soft = soft
        self.rng = np.random.default_rng()

    def update(self, episode):
        G = 0
        w = 1
        for s, a, r, s1, pos_moves in reversed(episode):
            G += r
            self.weights[s] = self.weights.get(s, [0.0 for _ in range(pos_moves)])
            self.weights[s][a] += w
            self.q[s] = self.q.get(s, np.array([1500.0 for _ in range(pos_moves)]))
            self.q[s][a] += w / self.weights[s][a] * (G - self.q[s][a])

            if a != self.action(s, pos_moves, optimal=True):
                break
            if self.soft != "Sampling":
                w = w / (1 - self.soft * ((pos_moves-1)/pos_moves))
            else:
                w = w / np.max(self.softmax(self.q[s]))
