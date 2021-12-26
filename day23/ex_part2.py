"""
Didn't expect that. Let's hack our way...

Test:


#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########


Puzzle:

#############
#...........#
###B#C#A#B###
  #D#C#B#A#
  #D#B#A#C#
  #C#D#D#A#
  #########


We'll define the graph positions (in hex digits), total of 23 valid slots:

01 2 3 4 56   <-- add 0x10 to each digit
  0 4 8 C
  1 5 9 D
  2 6 A E
  3 7 B F

"""

N = 23  # number of slots
cost_db = [1, 10, 100, 1000]
Amphipod = int  # EMPTY_SLOT=-1, 0=A, 1=B, 2=C, 3=D
State = list[Amphipod]  # per slot, who is there
EMPTY_SLOT = -1


def print_state(state: State):
    s = """\
#############
#gh.i.j.k.lm#
###0#4#8#c###
  #1#5#9#d#
  #2#6#a#e#
  #3#7#b#f#
  #########
"""
    for i in range(N):
        c = str(i) if i < 10 else chr(ord("a") + i - 10)
        s = s.replace(c, chr(state[i] + 65) if state[i] != EMPTY_SLOT else ".")
    print(s)


hallway_to_room_mapping = {
    0x10: [
        [0x11],
        [0x11, 0x12],
        [0x11, 0x12, 0x13],
        [0x11, 0x12, 0x13, 0x14],
    ],  # starting at slot 0x10, path reaching to any destination room
    0x11: [[], [0x12], [0x12, 0x13], [0x12, 0x13, 0x14]],
    0x12: [[], [], [0x13], [0x13, 0x14]],
    0x13: [[0x12], [], [], [0x14]],
    0x14: [[0x13, 0x12], [0x13], [], []],
    0x15: [[0x14, 0x13, 0x12], [0x14, 0x13], [0x14], []],
    0x16: [[0x15, 0x14, 0x13, 0x12], [0x15, 0x14, 0x13], [0x15, 0x14], [0x15]],
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
        or from_slot in (0x12, 0x13, 0x14)
        or to_slot in (0x12, 0x13, 0x14)
        else 1
    )
    return cost * weight


def can_exit_room(state: State, slot: int) -> bool:
    """
    Return True if amphipod can escape a room because all amphipods are in their place
    Not exhaustive! If there are amphipods above it, it may still be stuck
    """
    amphipod = state[slot]
    assert amphipod != EMPTY_SLOT
    room = slot // 4
    bottom_amphipod = state[room * 4 + 3]
    if bottom_amphipod != room:
        return True
    assert bottom_amphipod != EMPTY_SLOT
    for i in range(room * 4 + 2, room * 4 - 1, -1):
        if state[i] == EMPTY_SLOT:
            return False
        if state[i] != bottom_amphipod:
            return True
    return False


def find_all_moves_from_slot(state_in: State, slot: int) -> list[int]:
    """
    For a given amphipod at a given slot,
    return the cost of moving it into any other slot (a vector of 15 elements).
    In this vector, -1 is an invalid destination
    """
    r = [0] * N  # vector of costs to be returned. 0 if position not to be executed
    state = state_in[:]  # keep state_in immutable
    assert state[slot] != EMPTY_SLOT
    cost = 0
    amphipod = state[slot]
    if slot < 0x10:  # in a room?
        if not can_exit_room(state, slot):
            return r
        while slot % 4 > 0:
            # bubble up
            new_cost = move_single(state, amphipod, slot, slot - 1)
            if new_cost == 0:
                return r  # slot is occupied
            cost += new_cost
            slot -= 1
        assert slot % 4 == 0  # make sure we're at the top of the root
        hallway_left = slot // 4 + 0x11
        lslot = slot  # going left
        lcost = cost
        for i in range(hallway_left, 0x10 - 1, -1):
            move_cost = move_single(state, amphipod, lslot, i)
            if move_cost == 0:
                break
            lcost += move_cost
            lslot = i
            r[lslot] = lcost
        rslot = slot
        rcost = cost
        for i in range(hallway_left + 1, 0x16 + 1):
            move_cost = move_single(state, amphipod, rslot, i)
            if move_cost == 0:
                break
            rcost += move_cost
            rslot = i
            r[rslot] = rcost
    else:  # hallway
        assert slot >= 0x10
        # Our amphipod can only reach its designated room
        # and only if all others are the same amphipod species
        if any(
            [
                state[x] not in (EMPTY_SLOT, amphipod)
                for x in range(amphipod * 4, amphipod * 4 + 4)
            ]
        ):
            return r
        path_to_room = hallway_to_room_mapping[slot][amphipod] + [amphipod * 4]
        for next_slot in path_to_room:
            move_cost = move_single(state, amphipod, slot, next_slot)
            if move_cost == 0:
                return r
            cost += move_cost
            slot = next_slot
        assert slot == amphipod * 4
        for i in range(3):
            move_down_cost = move_single(state, amphipod, slot, slot + 1)
            if move_down_cost == 0:
                break
            cost += move_down_cost
            slot += 1
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
    return state[:16] == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]


best_cost = 100000000


def search(state: State, cost_in: int, depth: int) -> None:
    # print_state(state)
    global best_cost
    if is_solved(state):
        if cost_in < best_cost:
            print("Found solution having cost", cost_in)
        best_cost = min(cost_in, best_cost)
        return
    if depth == 100:
        for i in range(N):
            print(i, state[i])
        breakpoint()
    moves = find_all_moves(state)
    for move_cost in sorted(moves.keys()):
        new_cost = cost_in + move_cost
        if new_cost >= best_cost:
            break  # prune search. We already have a better solution
        for from_slot, to_slot in moves[move_cost]:
            next_state = state[:]
            # print(f'{depth}: {from_slot}->{to_slot} amphipod: {chr(state[from_slot]+65)}, cost: {new_cost}')
            next_state[to_slot] = next_state[from_slot]
            next_state[from_slot] = EMPTY_SLOT
            search(next_state, new_cost, depth + 1)


# TEST
#state = [EMPTY_SLOT] * N
#state[:16] = [1, 3, 3, 0, 2, 2, 1, 3, 1, 1, 0, 2, 3, 0, 2, 0]

# REAL
state = [EMPTY_SLOT] * N
state[:8] = [1, 3, 3, 2, 2, 2, 1, 3, 0, 1, 0, 3, 1, 0, 2, 0]

print_state(state)
search(state, 0, depth=0)

# state = [EMPTY_SLOT] * N
# state[4:8] = [EMPTY_SLOT, 1, 0, 1]
# print_state(state)
# r = find_all_moves_from_slot(state, 5)
# for i in range(N):
#     print(i, r[i])
