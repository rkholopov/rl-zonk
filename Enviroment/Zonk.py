import random

class Zonk:
    def __init__(self):
        self.state = sorted([random.randint(1, 6) for i in range(6)])
        self.score = 0
    def reset(self):
        self.state = sorted([random.randint(1, 6) for i in range(6)])
        self.score = 0
        return self.state, self.score
    def step(self, action):
        if action == '-1' and self.score >= 300:
            return -1, 0, True

        c = []
        for i in range(len(action)):
            if action[i] == '1':
                c.append(self.state[i])

        best = 0

        if len(c) == 6 and c[0] == c[1] - 1 == c[2] - 2 == c[3] - 3 == c[4] - 4 == c[5] - 5:
            best = 1500
        if len(c) == 6 and c[0] == c[1] and c[2] == c[3] and c[4] == c[5] and c[1]!=c[2] and c[3]!=c[4]:
            best = max(best, 750)
        if len(c) == 6 and c[0] == c[1] == c[2] and c[3] == c[4] == c[5]:
            if c[0] == 1:
                best = max(best, c[0] * 1000 + c[3] * 100)

        if c.count(1) >= 3:
            best = max(best, 1000 * (c.count(1) - 2) + 50 * c.count(5))

        if c.count(2) >= 3:
            best = max(best, 200 * (c.count(2) - 2) + 50 * c.count(5) + 100 * c.count(1))

        if c.count(3) >= 3:
            best = max(best, 300 * (c.count(3) - 2) + 50 * c.count(5) + 100 * c.count(1))

        if c.count(4) >= 3:
            best = max(best, 400 * (c.count(4) - 2) + 50 * c.count(5) + 100 * c.count(1))

        if c.count(5) >= 3:
            best = max(best, 500 * (c.count(5) - 2) + 100 * c.count(1))

        if c.count(6) >= 3:
            best = max(best, 600 * (c.count(6) - 2) + 50 * c.count(5) + 100 * c.count(1))

        best = max(best, 50 * c.count(5) + 100 * c.count(1))


        if best == 0:
            return -1, -self.score, True
        else:
            if len(self.state)-len(c)==0:
                self.state = sorted([random.randint(1, 6) for i in range(6)])
            else:
                self.state = sorted([random.randint(1, 6) for i in range(len(self.state)-len(c))])
            self.score += best
            return tuple([self.state, self.score]), best, False