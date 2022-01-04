import numpy as np

EMPTY = 0
RIGHT = 1
DOWN = 2

def read_world(fname: str) -> np.ndarray:
    r: list[list[int]] = []
    with open(fname) as f:
        for line in f:
            options={'>': RIGHT, 'v': DOWN, '.': EMPTY}
            v = [options[x] for x in line.strip()]
            r.append(v)
    return np.array(r, dtype=np.uint8)

def simulate_1_tick(world: np.ndarray) -> tuple[np.ndarray, bool]:
    Y,X = world.shape
    # we don't need to copy if we go from left to right...
    right_result = np.zeros(world.shape, dtype=np.uint8) # 0=EMPTY
    end_of_the_world = True
    for y in range(Y):
        for x in range(X):
            w = world[y, x]
            if w == RIGHT and world[y, (x+1) % X] == EMPTY:
                right_result[y, (x+1) % X] = w
                end_of_the_world = False
            elif w != EMPTY:
                right_result[y, x] = w
    down_result = np.zeros(world.shape, dtype=np.uint8)
    for y in range(Y):
        for x in range(X):
            w = right_result[y, x]
            if w == DOWN and right_result[(y+1) % Y, x] == EMPTY:
                down_result[(y+1) % Y, x] = w
                end_of_the_world = False
            elif w != EMPTY:
                down_result[y,x] = w
    return down_result, end_of_the_world


#
# MAIN
#

world = read_world('data.txt')
for i in range(10000):
    world, end_of_the_world = simulate_1_tick(world)
    if end_of_the_world:
        print('Iterations:', i+1)
        break
else:
    print("FAILED!")
