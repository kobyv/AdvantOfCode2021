import math

input = """\
Time:        59     79     65     75
Distance:   597   1234   1032   1328""".splitlines()


example = """\
Time:      7  15   30
Distance:  9  40  200""".splitlines()


# input = example
time_list = [int(x) for x in input[0].split(":")[1].split(" ") if x.strip()]
dist_list = [int(x) for x in input[1].split(":")[1].split(" ") if x.strip()]

prod_winning_options = 1
for t, d in zip(time_list, dist_list):
    winning_options = 0
    for i in range(1, t):
        my_d = i * (t - i)
        if my_d > d:
            winning_options += 1
    print(winning_options)
    prod_winning_options *= winning_options

print("Part 1:", prod_winning_options)

# PART 2

# t = 71530
# d = 940200

t = 59796575
d = 597123410321328

# Quadratic equation:
# x*(t-x) - d > 0
# ==> x^2 - xt + d < 0
# x1,2 before integering = 0.5*(t ± sqrt(t^2 - 4d))

Q = math.sqrt(t * t - d * 4)
x1 = 0.5 * (t + Q)
x2 = 0.5 * (t - Q)

formula = lambda x: x**2 - x * t + d
x1, x2 = sorted([x1, x2])
x1, x2 = int(x1), int(x2)
if formula(x1) > 0:
    x1 += 1
if formula(x2) > 0:
    x2 += 1

print("===")
print(x1, x2)
print("PART 2: ", x2 - x1 + 1)
