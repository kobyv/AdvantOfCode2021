import numpy as np


def scan_horizontal(m, vm, y, x1, x2, dx):
    max_h = ' '  # smaller than '0'
    for x in range(x1,x2,dx):
        if m[y][x] > max_h:
            vm[y][x] = 1
            max_h = m[y][x]

def scan_vertical(m, vm, x, y1, y2, dy):
    max_h = ' '  # smaller than '0'
    for y in range(y1,y2,dy):
        if m[y][x] > max_h:
            vm[y][x] = 1
            max_h = m[y][x]


m: list[str] = []  # the input height map

with open('input.txt') as f:
    for line in f:
        m.append(line.strip())
Y = len(m); X = len(m[0])

vm = np.zeros((Y,X), dtype=int) # visibility map

for y in range(Y):
    scan_horizontal(m, vm, y, 0, X, 1)      # right
    scan_horizontal(m, vm, y, X-1, -1, -1)  # left

for x in range(X):
    scan_vertical(m, vm, x, 0, Y, 1)        # down
    scan_vertical(m, vm, x, Y-1, -1, -1)    # up

print('Visible trees:', sum(sum(vm)))

# -- Part Two --

def scan2_horizontal(m, y, x1, x2, dx):
    ref_h = m[y][x1]
    for x in range(x1+dx,x2,dx):
        if m[y][x] >= ref_h:
            return (x - x1) * dx
    return (x2 - x1) * dx - 1

def scan2_vertical(m, x, y1, y2, dy):
    ref_h = m[y1][x]
    for y in range(y1+dy,y2,dy):
        if m[y][x] >= ref_h:
            return (y - y1) * dy
    return (y2 - y1) * dy - 1

best_score = 0
for y in range(Y):
    for x in range(X):
        r = scan2_horizontal(m, y, x, X, 1)
        l = scan2_horizontal(m, y, x, -1, -1)
        d = scan2_vertical(m, x, y, Y, 1)
        u = scan2_vertical(m, x, y, -1, -1)
        score = r * l * d * u
        best_score = max(best_score, score)

print('PART 2. scenic score:', best_score)
