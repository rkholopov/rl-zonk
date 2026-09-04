from functools import lru_cache
import pandas as pd


@lru_cache(None)
def reward(x, k, show_distribution=False):
    if k == 6 and x >= 16450:
        return x
    if k == 5 and x >= 3050:
        return x
    if k == 4 and x >= 1050:
        return x
    if k == 3 and x >= 400:
        return x
    if k < 3 and x >= 300:
        return x
    distribution = []
    m = 0
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            for i3 in range(1, 7):
                for i4 in range(1, 7):
                    for i5 in range(1, 7):
                        for i6 in range(1, 7):
                            best = 0
                            c = sorted([i1, i2+9*(k < 2), i3+9*(k < 3), i4+9*(k < 4), i5+9*(k < 5), i6+9*(k < 6)])

                            if c[-1] <= 10:
                                if c[0] == c[1] - 1 == c[2] - 2 == c[3] - 3 == c[4] - 4 == c[5] - 5 and k == 6:
                                    best = reward(x+1500,6)
                                if c[0] == c[1] and c[2] == c[3] and c[4] == c[5] and k == 6:
                                    best = max(best, reward(x+750, 6))
                                if c[0] == c[1] == c[2] and c[3] == c[4] == c[5] and k == 6:
                                    if c[0] == 1:
                                        best = max(best, reward(x+c[0]*1000+c[3]*100, 6))
                                    else:
                                        best = max(best, reward(x+c[0]*100+c[3]*100, 6))

                                if c.count(1) >= 3:
                                    y = 1000 * (c.count(1) - 2) + 50 * c.count(5)
                                    if c.count(5) + c.count(1) == k:
                                        best = max(best, reward(x+y, 6))
                                    else:
                                        best = max(best, reward(x+y, k-c.count(1)-c.count(5)))

                                if c.count(2) >= 3:
                                    y = 200 * (c.count(2) - 2) + 50 * c.count(5) + 100 * c.count(1)
                                    if c.count(5) + c.count(1) + c.count(2) == k:
                                        best = max(best, reward(x+y, 6))
                                    else:
                                        best = max(best, reward(x+y, k-c.count(1)-c.count(5)-c.count(2)))

                                if c.count(3) >= 3:
                                    y = 300 * (c.count(3) - 2) + 50 * c.count(5) + 100 * c.count(1)
                                    if c.count(5) + c.count(1) + c.count(3) == k and x + y < 16450:
                                        best = max(best, reward(x+y, 6))
                                    else:
                                        best = max(best, reward(x+y, k-c.count(1)-c.count(5)-c.count(3)))

                                if c.count(4) >= 3:
                                    y = 400 * (c.count(4) - 2) + 50 * c.count(5) + 100 * c.count(1)
                                    if c.count(5) + c.count(1) + c.count(4) == k and x + y < 16450:
                                        best = max(best, reward(x+y, 6))
                                    else:
                                        best = max(best, reward(x+y, k-c.count(1)-c.count(5)-c.count(4)))

                                if c.count(5) >= 3:
                                    y = 500 * (c.count(5) - 2) + 100 * c.count(1)
                                    if c.count(5) + c.count(1) == k and x + y < 16450:
                                        best = max(best, reward(x+y, 6))
                                    else:
                                        best = max(best, reward(x+y, k-c.count(1)-c.count(5)))

                                if c.count(6) >= 3:
                                    y = 600 * (c.count(6) - 2) + 50 * c.count(5) + 100 * c.count(1)
                                    if c.count(6) + c.count(1) + c.count(5) == k and x + y < 16450:
                                        best = max(best, reward(x+y, 6))
                                    else:
                                        best = max(best, reward(x+y, k-c.count(1)-c.count(5)-c.count(6)))

                                y = 50 * c.count(5) + 100 * c.count(1)
                                if c.count(1) + c.count(5) == k and k <= 4:
                                    best = max(best, reward(x + y, 6))
                                elif y > 0:
                                    best = max(best, reward(x+y, k-c.count(1)-c.count(5)))

                                if best != x:
                                    distribution.append(best)
                                    m += best / 6 ** k
                                else:
                                    distribution.append(0)

    if show_distribution:
        return m, sorted(distribution)
    else:
        return m


'''
start = 0
r, dist = reward(start, 6, show_distribution=True)
pd.DataFrame(dist).to_excel('Distribution_of_SBME.xlsx', index=False, header=False)

print(dist)
print(start, r-start)
'''
