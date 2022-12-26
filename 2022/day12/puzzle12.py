import numpy as np
import sys

hmap: list[list[int]] = []

Coord = tuple[int, int]
S_pos = (-1, -1)
E_pos = (-1, -1)

with open("input.txt") as f:
    for y, line in enumerate(f):
        line = line.strip()
        line_int = [ord(c) - ord("a") for c in line]
        if "S" in line:
            x = line.index("S")
            S_pos = (y, x)
            line_int[x] = 0
        if "E" in line:
            x = line.index("E")
            E_pos = (y, x)
            line_int[x] = ord("z") - ord("a")
        hmap.append(line_int)
assert S_pos != (-1, -1)
assert E_pos != (-1, -1)

# print(hmap)
# print(S_pos, E_pos)
Y = len(hmap)
X = len(hmap[0])


def visit(y, x, dir_y, dir_x, steps, visiting_queue):
    y2 = y + dir_y
    x2 = x + dir_x
    if not 0 <= y2 < Y or not 0 <= x2 < X:
        return
    if hmap[y2][x2] - hmap[y][x] > 1:
        return
    visiting_queue.append(((y2, x2), steps, (y, x)))


def walk(starting_pos):
    "Breadth First Search"
    visited = np.ones((Y, X), dtype="int") * 1000000

    visiting_queue: list[tuple[Coord, int, Coord]] = [(starting_pos, 0, starting_pos)]

    while visiting_queue:
        # print(visiting_queue)
        ((y, x), steps, (py, px)) = visiting_queue[0]
        visiting_queue = visiting_queue[1:]
        if visited[(y, x)] <= steps:
            steps = visited[(y, x)]
            continue
        visited[(y, x)] = steps
        if (y, x) == E_pos:
            continue
        steps += 1
        visit(y, x, -1, 0, steps, visiting_queue)  # UP
        visit(y, x, 1, 0, steps, visiting_queue)  # DOWN
        visit(y, x, 0, -1, steps, visiting_queue)  # LEFT
        visit(y, x, 0, +1, steps, visiting_queue)  # RIGHT

    return visited[E_pos]


n = walk(S_pos)
print("Part 1:", n)

# -- PART 2 --

min_n = 100000
for y in range(Y):
    for x in range(X):
        if hmap[y][x] == 0:
            n = walk((y, x))
            min_n = min(min_n, n)
print("Part 2:", min_n)
