"""
Test:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########


Puzzle:

#############
#...........#
###B#C#A#B###
  #C#D#D#A#
  #########


We'll define the graph positions (in hex digits), total of 15 valid slots:

89 A B C DE
  0 2 4 6
  1 3 5 7

The weight of 9-A, A-B, B-C, C-D, 0-{9,A}, 2-{A,B}, 4-{C,B}, 6-{C,D} is 2

"""

N = 15  # number of slots
cost_db = [1, 10, 100, 1000]
Amphipod = int  # EMPTY_SLOT=-1, 0=A, 1=B, 2=C, 3=D
State = list[Amphipod]  # per slot, who is there
EMPTY_SLOT = -1

def print_state(state: State):
    s = '''\
#############
#89.a.b.c.de#
  #0#2#4#6#
  #1#3#5#7#
  #########
'''
    for i in range(N):
        s = s.replace(f'{i:x}', chr(state[i]+65) if state[i] != EMPTY_SLOT else '.')
    print(s)

hallway_to_room_mapping = {
    8: [
        [9],
        [9, 10],
        [9, 10, 11],
        [9, 10, 11, 12],
    ],  # starting at slot 8, path reaching to any destination room
    9: [[], [10], [10, 11], [10, 11, 12]],
    10: [[], [], [11], [11, 12]],
    11: [[10], [], [], [12]],
    12: [[11, 10], [11], [], []],
    13: [[12, 11, 10], [12, 11], [12], []],
    14: [[13, 12, 11, 10], [13, 12, 11], [13, 12], [13]],
}


def move_single(state: State, amphipod: Amphipod, from_slot: int, to_slot: int) -> int:
    """
    Movement must be valid in the graph
    Return the movement cost
    """
    if state[to_slot] != EMPTY_SLOT:
        return 0
    cost = cost_db[amphipod]

    # did we move 2 positions or 1?
    # two positions if between room and hallway, or in the hallway except for edges
    weight = (
        2
        if abs(from_slot - to_slot) > 1
        or from_slot in (10, 11, 12)
        or to_slot in (10, 11, 12)
        else 1
    )
    return cost * weight


def find_all_moves_from_slot(state_in: State, slot: int) -> list[int]:
    """
    For a given amphipod at a given slot,
    return the cost of moving it into any other slot (a vector of 15 elements).
    In this vector, -1 is an invalid destination
    """
    r = [0] * N  # vector of costs to be returned. 0 if position not to be executed
    state = state_in[:]  # keep state_in immutable
    assert(state[slot] != EMPTY_SLOT)
    cost = 0
    amphipod = state[slot]
    if slot in (1, 3, 5, 7):  # lower part of a room
        if (slot - 1) // 2 == amphipod:
            return r  # an amphipod that belongs to this place is here
        cost = move_single(state, amphipod, slot, slot - 1)
        if cost == 0:
            return r  # slot is occupied
        slot -= 1
    if slot in (0, 2, 4, 6):  # upper part of the room
        if slot // 2 == amphipod and state[slot+1] == amphipod:
            return r  # an amphipod that belongs to this place is here
        hallway_left = slot // 2 + 9
        lslot = slot  # going left
        lcost = cost
        for i in range(hallway_left, 8 - 1, -1):
            move_cost = move_single(state, amphipod, lslot, i)
            if move_cost == 0:
                break
            lcost += move_cost
            lslot = i
            r[lslot] = lcost
        rslot = slot
        rcost = cost
        for i in range(hallway_left + 1, 14 + 1):
            move_cost = move_single(state, amphipod, rslot, i)
            if move_cost == 0:
                break
            rcost += move_cost
            rslot = i
            r[rslot] = rcost
    else:  # hallway
        # Our amphipod can only reach its designated room
        if state[amphipod*2+1] not in (EMPTY_SLOT, amphipod):  # bottom amphipod in destination room does not match
            return r
        path_to_room = hallway_to_room_mapping[slot][amphipod] + [amphipod * 2]
        for next_slot in path_to_room:
            move_cost = move_single(state, amphipod, slot, next_slot)
            if move_cost == 0:
                return r
            cost += move_cost
            slot = next_slot
        assert slot == amphipod * 2
        move_down_cost = move_single(state, amphipod, slot, slot + 1)
        if move_down_cost > 0:
            r[slot + 1] = cost + move_down_cost  # reached the bottom of the room
        else:
            r[slot] = cost  # bottom is occupied. Rest at the roof

    return r


def find_all_moves(state: State):
    cost_table = {}
    for slot in range(N):
        if state[slot] != EMPTY_SLOT:
            cost_vector = find_all_moves_from_slot(state, slot)
            for to_slot, cost in enumerate(cost_vector):
                if cost > 0:
                    if not cost in cost_table:
                        cost_table[cost] = []
                    cost_table[cost].append((slot, to_slot))
    return cost_table


def is_solved(state: State):
    return (
        state[0] == 0
        and state[1] == 0
        and state[2] == 1
        and state[3] == 1
        and state[4] == 2
        and state[5] == 2
        and state[6] == 3
        and state[7] == 3
    )


best_cost = 100000000


def search(state: State, cost_in: int, depth: int) -> None:
    #print_state(state)
    global best_cost
    if is_solved(state):
        if cost_in < best_cost:
            print("Found solution having cost", cost_in)
        best_cost = min(cost_in, best_cost)
        return
    if depth == 100:
        for i in range(N):
            print(i,state[i])
        breakpoint()
    moves = find_all_moves(state)
    for move_cost in sorted(moves.keys()):
        new_cost = cost_in + move_cost
        if new_cost >= best_cost:
            break  # prune search. We already have a better solution
        for from_slot, to_slot in moves[move_cost]:
            next_state = state[:]
            #print(f'{depth}: {from_slot}->{to_slot} amphipod: {chr(state[from_slot]+65)}, cost: {new_cost}')
            next_state[to_slot] = next_state[from_slot]
            next_state[from_slot] = EMPTY_SLOT
            search(next_state, new_cost, depth+1)


# TEST
#state = [EMPTY_SLOT] * N
#state[:8] = [1, 0, 2, 3, 1, 2, 3, 0]

state = [EMPTY_SLOT] * N
state[:8] = [1, 2, 2, 3, 0, 3, 1, 0]

print_state(state)

search(state, 0, depth=0)

# state = [EMPTY_SLOT] * N
# state[5] = 3
# #state[9] = 1
# #state[12] = 2
# r = find_all_moves_from_slot(state, 5)
# for i in range(N):
#     print(i,r[i])
