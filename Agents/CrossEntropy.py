from Agents.Baseline import Baseline
import numpy as np


class CrossEntropy(Baseline):
    def __init__(self, soft, alpha, percentile):
        super().__init__(soft, alpha, percentile)
        self.soft = 0.1 if soft == "Sampling" else soft
        self.percentile = percentile
        self.policy = {}
        self.rng = np.random.default_rng()
        self.train = []
        self.rewards = []

    def action(self, state, pos_moves, optimal=False):
        if state not in self.policy:
            return 0 if optimal else self.rng.choice([i for i in range(pos_moves)])
        if optimal:
            return np.argmax(self.policy[state])
        probabilities = self.policy[state] / sum(self.policy[state])
        probabilities = (1 - self.soft) * probabilities + self.soft / pos_moves
        return self.rng.choice(pos_moves, p=probabilities)

    def update(self, episode):
        self.train.append(episode)
        self.rewards.append(sum([r for s, a, r, a1, p in episode]))
        if len(self.rewards) >= 10**4:
            for i in self.policy.keys():
                self.policy[i] = self.policy[i] / 2
            percentile = np.percentile(np.array(self.rewards), self.percentile)

            for i in range(len(self.rewards)):
                if self.rewards[i] >= percentile:
                    for j in range(len(self.train[i])):
                        s, a, r, a1, p = self.train[i][j]
                        self.policy[s] = self.policy.get(s, np.array([0.0 for _ in range(p)]))
                        self.policy[s][a] += 1

            self.rewards = []
            self.train = []
