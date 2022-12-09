Point = tuple[int, int]

def get_step(d: int) -> int:
    ''' given delta movement, return its unit step '''
    if d == 0:
        return 0
    return d // abs(d)

def move_tail(H: Point, T: Point) -> Point:
    T0 = T
    diff = (H[0] - T[0], H[1] - T[1])
    if abs(diff[0]) == 2 or abs(diff[1]) == 2:
        step_x = get_step(diff[0])
        step_y = get_step(diff[1])
        T = (T[0] + step_x, T[1] + step_y)
    if abs(T[0] - H[0]) > 1 or abs(T[1] - H[1]) > 1:
        print('hi')
    return T


H = (0,0)
T = (0,0)
visited_set = set()

with open('input.txt') as f:
    for instruction in f:
        (direction, amount) = instruction.strip().split()
        for _ in range(int(amount)):
            if direction == 'R':
                H = (H[0] + 1, H[1])
            elif direction == 'L':
                H = (H[0] - 1, H[1])
            elif direction == 'U':
                H = (H[0], H[1] + 1)
            elif direction == 'D':
                H = (H[0], H[1] - 1)
            else:
                assert False
            
            T = move_tail(H, T)
            visited_set.add(T)

print("Visited positions:", len(visited_set))

# -- PART 2 --
H = (0,0)
tail = [(0,0)]*9
visited_set = set()

with open('input.txt') as f:
    for instruction in f:
        (direction, amount) = instruction.strip().split()
        for _ in range(int(amount)):
            if direction == 'R':
                H = (H[0] + 1, H[1])
            elif direction == 'L':
                H = (H[0] - 1, H[1])
            elif direction == 'U':
                H = (H[0], H[1] + 1)
            elif direction == 'D':
                H = (H[0], H[1] - 1)
            else:
                assert False

            tail[0] = move_tail(H, tail[0])
            for i in range(len(tail) - 1):
                tail[i+1] = move_tail(tail[i], tail[i+1])
            visited_set.add(tail[-1])

print("PART 2. Visited positions:", len(visited_set))
