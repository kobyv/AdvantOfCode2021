# %%


def round_func(z: int, w: int, should_div: bool, arg1: int, arg2: int) -> int:
    x = z
    x %= 26
    z = z // (26 if should_div else 1)
    x += arg1
    x = 1 if x != w else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = w
    y += arg2
    y *= x
    return z + y


def search(z_target, should_div: bool, arg1: int, arg2: int):
    print(len(z_target), min(z_target), max(z_target))
    z_solved = set([])
    for w in range(1, 10):
        for z in range(max(0, min(z_target) - 26), (max(z_target) + 2) * 26):
            r = round_func(z, w, should_div, arg1, arg2)
            if r in z_target:
                z_solved.add(z)
                # print(w,z,r)
    return z_solved


rounds = (
    (False, 13, 0),  # 0
    (False, 11, 3),  # 1
    (False, 14, 8),  # 2
    (True, -5, 5),  # 3
    (False, 14, 13),  # 4
    (False, 10, 9),  # 5
    (False, 12, 6),  # 6
    (True, -14, 1),  # 7
    (True, -8, 1),  # 8
    (False, 13, 2),  # 9
    (True, 0, 7),  # 10
    (True, -5, 5),  # 11
    (True, -9, 8),  # 12
    (True, -1, 15),
)  # 13


z_target = [[] for i in range(15)]
z_target[14] = [0]
for i in range(13, 7, -1):
    p = rounds[i]
    z_target[i] = search(z_target[i + 1], p[0], p[1], p[2])

# %%
# Iterations

w_vec = [1] * 14


def iterate(n: int, z: int):
    valid_z = z_target[n + 1]
    p = rounds[n]
    for w in range(1, 10):
        # if w != int(digits[n]): continue
        w_vec[n] = w  # for printing only
        z_next = round_func(z, w, p[0], p[1], p[2])
        if n == 13:
            if z_next == 0:
                print("Solved!", ''.join([str(d) for d in w_vec]))
            continue
        if not valid_z or z_next in valid_z:
            iterate(n + 1, z_next)


iterate(0, 0)

