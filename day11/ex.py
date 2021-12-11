from copy import deepcopy
EDGE = -1000000
grid: list[list[int]] = [[EDGE] * 12]


def print_grid():
    for y in range(1, 11):
        print("".join([str(x) for x in grid[y][1:-1]]))
    print()


def simulate_one_step() -> int:
    "Return the number of flashes"
    num_flashes = 0
    to_be_visited = set([])

    def update(y, x):
        assert grid[y][x] <= 10
        if y in (0,11) or x in (0,11):  # not important
            return
        if grid[y][x] > 9:
            return
        grid[y][x] += 1
        if grid[y][x] == 10:
            to_be_visited.add((y, x))
            #print(f" Added to visit list: {y},{x}")

    def update_all(y, x):
        if grid[y][x] < 10:
            grid[y][x] += 1
        #print(f"In {y},{x}, value {grid[y][x]}")
        if grid[y][x] == 10:
            update(y - 1, x - 1)
            update(y - 1, x + 0)
            update(y - 1, x + 1)
            update(y + 0, x - 1)
            update(y + 0, x + 1)
            update(y + 1, x - 1)
            update(y + 1, x + 0)
            update(y + 1, x + 1)

    # Stage 1: traverse all grid
    for y in range(1, 11):
        for x in range(1, 11):
            to_be_visited.add((y,x))
    # Stage 2: chain reaction
    while len(to_be_visited):
        y, x = to_be_visited.pop()
        update_all(y, x)

    # Flash all
    for y in range(1, 11):
        for x in range(1, 11):
            if grid[y][x] > 9:
                num_flashes += 1
                grid[y][x] = 0
    return num_flashes


with open("data.txt") as f:
    for i, line in enumerate(f):
        l = [EDGE]
        for c in line.strip():
            l.append(int(c))
        l.append(EDGE)
        grid.append(l)
grid.append([EDGE] * 12)
grid_bk = deepcopy(grid)

print("INIT:")
print_grid()

total_flashes = 0
for i in range(100):
    total_flashes += simulate_one_step()
    print("*** AFTER step", i + 1)
    #print_grid()
print("Total flashes:", total_flashes)

########################################
print("PART 2")
grid = grid_bk
for i in range(10000):
    num_flashes = simulate_one_step()
    if num_flashes == 100:
        print('After step', i+1)
        break
else:
    assert(False)


