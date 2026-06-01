m = 251
x = 250
while m >= x:
    m = 0
    x += 50
    print(x)
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            best = 0
            c = sorted([i1, i2])

            y = 50 * c.count(5) + 100 * c.count(1)
            best = max(best, y + 380 * (c.count(5) + c.count(1) == 3 and x + y < 16450))
            if best != 0:
                m += (x + best) / 6 ** 2


print(x, m)  # 300 216.66666666666674
# При значении 300 и больше в раунде бросать три кубика невыгодно