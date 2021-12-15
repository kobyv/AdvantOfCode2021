import numpy as np
from typing import List, Tuple


def read_file() -> np.ndarray:
    risk = []
    with open("data.txt") as f:
        for line in f:
            v = [int(x) for x in line.strip()]
            risk.append(v)
    return np.array(risk, dtype="uint")


risk = read_file()


def flrp(total_risk: np.ndarray):
    "Find least risky path"
    queue: List[Tuple[int, int, int]] = [(0, 0, 0)]  # prev_risk, y, x
    sy, sx = total_risk.shape
    while queue:
        queue.sort()  # better to use heapq
        prev_risk, y, x = queue[0]
        queue = queue[1:]
        new_risk = prev_risk + risk[y, x]
        if total_risk[y, x] > 0 and new_risk >= total_risk[y, x]:
            continue
        total_risk[y, x] = new_risk
        if y > 0:
            queue.append((new_risk, y - 1, x))
        if y < sy - 1:
            queue.append((new_risk, y + 1, x))
        if x > 0:
            queue.append((new_risk, y, x - 1))
        if x < sx - 1:
            queue.append((new_risk, y, x + 1))


total_risk = np.zeros(
    risk.shape, dtype="uint"
)  # min accumulated risk till this point. 0: not yet visited
# find_least_risky_path(total_risk, 0, 0, 0)
flrp(total_risk)
# print(total_risk)
sy, sx = total_risk.shape
print("PART 1:", total_risk[sy - 1, sx - 1] - total_risk[0, 0])

################################
# PART 2
risk = risk - 1
risk0 = risk.copy()
for i in range(4):
    risk = np.hstack((risk, (risk0 + i + 1) % 9))
risk0 = risk.copy()
for i in range(4):
    risk = np.vstack((risk, (risk0 + i + 1) % 9))
risk = risk + 1

total_risk = np.zeros(
    risk.shape, dtype="uint"
)  # min accumulated risk till this point. 0: not yet visited
flrp(total_risk)
# print(total_risk)
sy, sx = total_risk.shape
print("PART 2:", total_risk[sy - 1, sx - 1] - total_risk[0, 0])

# with open('total_risk.csv', 'w') as f:
#     for y in range(sy):
#         for x in range(sx):
#             f.write(str(risk[y][x]))
#             if x != sx-1: f.write(',')
#         f.write('\n')
# print(total_risk[sy-3:,-10:])
