# %%
import numpy as np
from typing import Set

# %%
# We have 6 cube faces (sensor facing direction).
# For each face, we can have 4 rotation options.
# We'll start with XY face rotation, followed by all XZ rotations,
# followed by two YZ rotations

# fmt: off
rot_xy = np.array([
    [0,-1, 0],
    [1, 0, 0],
    [0, 0, 1]], dtype=np.int32)

rot_xz = np.array([
    [0, 0,-1],
    [0, 1, 0],
    [1, 0, 0]], dtype=np.int32)

rot_yz = np.array([
    [1, 0, 0],
    [0, 0,-1],
    [0, 1, 0]], dtype=np.int32)
# fmt: on

all_rot: list[np.ndarray] = []


def add_face_rotations(rot: np.ndarray) -> None:
    all_rot.append(rot)
    all_rot.append(rot_xy @ rot)
    all_rot.append(rot_xy @ rot_xy @ rot)
    all_rot.append(
        rot_xy @ rot_xy @ rot_xy @ rot
    )  # can do rot_xy.transpose(), not really shorter...


def generate_all_rotations() -> None:
    add_face_rotations(np.eye(3, dtype="int32"))
    add_face_rotations(rot_xz)
    add_face_rotations(rot_xz @ rot_xz)
    add_face_rotations(rot_xz @ rot_xz @ rot_xz)
    add_face_rotations(rot_yz)
    add_face_rotations(rot_yz @ rot_yz @ rot_yz)


def count_matching_beacons(s1, s2) -> int:
    """
    Given all beacon points of scanner 1 and scanner 2 fully aligned,
    how many are overlapping?

    s1,s2: np.ndarray([b1,b2,b3,...])  # array of beacon locations
    """
    cnt = 0
    for b1 in s1:
        for b2 in s2:
            if np.array_equal(b1, b2):
                cnt += 1
    return cnt


def match_two_scanners(s1, s2):
    """
    Given point list of two scanners, try to align them
    such that we get at least 12 matching beacons.
    They cannot be more than 19 units apart in each axis:

    Returns: (rotated and translated s2, distance for part 2)
    """
    for rot in all_rot:
        # Find all possible offsets (between any two beacons)
        s2_rot = s2 @ rot
        for b1 in s1:
            for b2 in s2_rot:
                d = b1 - b2  # d is the position of s2 relative to s1
                c = count_matching_beacons(s1, s2_rot + d)
                if c >= 12:
                    return (s2_rot + d, d)
    return (None, None)


def read_file(fname: str) -> list[np.ndarray]:
    all_scanners: list[np.ndarray] = []
    l: list[list[int]] = []
    with open(fname) as f:
        for line in f:
            if line[:3] == "---":  # --- scanner X ---
                continue
            elif not line.strip():  # spacer between scanner lists
                if l:
                    all_scanners.append(np.array(l, dtype=np.int32))
                    l = []
            else:
                sx, sy, sz = line.strip().split(",")
                x, y, z = int(sx), int(sy), int(sz)
                l.append([x, y, z])
    all_scanners.append(np.array(l, dtype=np.int32))
    return all_scanners


# %%
#
# MAIN
#

generate_all_rotations()
all_scanners = read_file("data.txt")
N = len(all_scanners)
locations = np.zeros((N, 3), dtype=np.int32)  # for part 2
matched: list[bool] = [True] + [False] * (N - 1)
queue: list[int] = [0]
while len(queue):
    i1 = queue[0]
    queue = queue[1:]
    print(f"Processing scanner {i1}")
    for i2 in range(N):
        if matched[i2]:
            continue
        candidate, dist = match_two_scanners(all_scanners[i1], all_scanners[i2])
        if not candidate is None:
            # we have at least 12 matches
            all_scanners[i2] = candidate
            matched[i2] = True
            queue.append(i2)
            locations[i2] = dist
            print(f"    Scanner {i2} is located at {dist}")

if not all(matched):
    print("Not all scanners are matched!!")

# Count unique number of beacon
all_beacons: Set[str] = set()  # np.unique may be better
for s in all_scanners:
    for b in s:
        all_beacons.add(str(b))
print("** PART 1 **\nNumber of beacons:", len(all_beacons))

# %%
# PART 2

max_dist = 0
for s1 in range(N):
    for s2 in range(N):
        d = np.sum(np.abs(locations[s1] - locations[s2]))
        max_dist = max(max_dist, d)
print("** PART 2**\nMax L1 distance:", max_dist)
# %%
