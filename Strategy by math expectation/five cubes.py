m = 251
x = 250
while m >= x:
    m = 0
    x += 50
    print(x)
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            for i3 in range(1, 7):
                for i4 in range(1, 7):
                    for i5 in range(1, 7):
                        best = 0
                        c = sorted([i1, i2, i3, i4, i5])
                        if c.count(1) >= 3:
                            y = 1000 * (c.count(1) - 2) + 50 * c.count(5)
                            best = max(best, y + 380 * (c.count(5)+c.count(1)==5 and x+y<16450))

                        if c.count(2) >= 3:
                            y = 200 * (c.count(2) - 2) + 50 * c.count(5) + 100 * c.count(1)
                            best = max(best, y + 380 * (c.count(5)+c.count(1)+c.count(2)==5 and x+y<16450))

                        if c.count(3) >= 3:
                            y = 300 * (c.count(3) - 2) + 50 * c.count(5) + 100 * c.count(1)
                            best = max(best, y + 380 * (c.count(5) + c.count(1) + c.count(3) == 5 and x + y < 16450))

                        if c.count(4) >= 3:
                            y = 400 * (c.count(4) - 2) + 50 * c.count(5) + 100 * c.count(1)
                            best = max(best, y + 380 * (c.count(5) + c.count(1) + c.count(4) == 5 and x + y < 16450))

                        if c.count(5) >= 3:
                            y = 500 * (c.count(5) - 2) + 100 * c.count(1)
                            best = max(best, y + 380 * (c.count(5) + c.count(1) == 5 and x + y < 16450))

                        if c.count(6) >= 3:
                            y = 600 * (c.count(6) - 2) + 50 * c.count(5) + 100 * c.count(1)
                            best = max(best, y + 380 * (c.count(6) + c.count(1) + c.count(5) == 5 and x + y < 16450))

                        best = max(best, 50 * c.count(5) + 100 * c.count(1))
                        if best != 0:
                            m += (x + best) / 6 ** 5

print(x, m)  # 3100 3097.740483539295
# При значении 3100 и больше в раунде бросать пять кубиков невыгодно