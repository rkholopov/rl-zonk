import random


class Zonk:
    def __init__(self):
        self.state = 6
        self.score = 0
    def reset(self):
        self.state = 6
        self.score = 0
        return tuple([self.state, self.score]), self.score, False
    def step(self, action):
        if action == '-1' and self.score >= 300:
            return -1, 0, True
        if action == '0':
            self.state = sorted([random.randint(1,6) for _ in range(self.state)])
            return self.state, 0, False

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
            if len(self.state)-len(c) == 0:
                self.state = 6
            else:
                self.state = len(self.state)-len(c)
            self.score += best
            return tuple([self.state, self.score]), best, False

    def find_possible_moves(self):
        c = self.state
        if isinstance(c, int):
            if self.score >= 300:
                ans = {0: '-1', 1: '0'}
            else:
                ans = {0: '0'}
            return ans

        ans = {0: '-1'}
        cnt = 1

        for i in range(1, 2**len(c)):
            x = i
            move = []
            for j in range(len(c)):
                move.append(str(x%2))
                x = x//2

            move = ''.join(move)
            s = []
            ok = True
            for j in range(len(move)):
                if move[j] == '1':
                    s.append(self.state[j])

            for j in range(2,7):
                if j!=5 and 0 < s.count(j) < 3:
                    ok = False

            if move=='111111':
                if s[0]==s[1]-1==s[2]-2==s[3]-3==s[4]-4==s[5]-5 or s[0]==s[1] and s[2]==s[3] and s[4]==s[5]:
                    ok = True

            if ok:
                ans[cnt] = move
                cnt += 1

        return ans
