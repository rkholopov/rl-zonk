import numpy as np


class Monte_Carlo():
    def __init__(self, soft):
        self.q = {}
        self.entries = {}
        self.soft = soft
        self.rng = np.random.default_rng()

    def action(self, state, pos_moves, optimal=False):
        self.q[state] = self.q.get(state, [[0] for _ in range(pos_moves)])
        if not(optimal) and self.rng.random() < self.soft:
            return self.rng.choice([i for i in range(pos_moves)])
        return int(np.argmax(self.q[state]))


    def update(self, episode):
        G = 0
        for s, a, r, s1, pos_moves in reversed(episode):
            G += r
            self.entries[s] = self.entries.get(s, [0 for _ in range(pos_moves)])
            self.entries[s][a] += 1
            self.q[s] = self.entries.get(s, [[1500] for _ in range(pos_moves)])
            self.q[s][a] += (G - self.q[s][a]) / self.entries[s][a]
