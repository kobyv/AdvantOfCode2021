from typing import List, Set, Tuple

Points = Set[Tuple[int, int]]


def apply_fold(pts: Points, fold: int) -> Points:
    r: Points = set()
    if fold >= 0:
        for p in pts:
            x, y = p
            assert x != fold
            folded_x = fold * 2 - x if x > fold else x
            r.add((folded_x, y))
    else:
        fold = -fold
        for p in pts:
            x, y = p
            assert y != fold
            folded_y = fold * 2 - y if y > fold else y
            r.add((x, folded_y))
    return r


def print_dots(pts: Points) -> None:
    x_size = max([p[0] for p in pts]) + 1
    y_size = max([p[1] for p in pts]) + 1
    for y in range(y_size):
        line = "".join(["X" if (x, y) in pts else " " for x in range(x_size)])
        print(line)


pts: Points = set()
folds: List[int] = []  # x-fold positive, y-fold negative

with open("data.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line[0] == "f":
            assert line.startswith("fold along ")
            axis_str, pos_str = line[11:].split("=")
            assert axis_str in ("x", "y")
            pos = int(pos_str)
            folds.append(pos if axis_str == "x" else -pos)
        else:
            xs, ys = line.strip().split(",")
            pts.add((int(xs), int(ys)))


r = apply_fold(pts, folds[0])
print("Points after first fold:", len(r))

print("PART 2")

for fold in folds[1:]:
    r = apply_fold(r, fold)
print_dots(r)
