import numpy as np

map = {}  # sorry for redefining the builtin type

with open("input.txt") as input:
    directions = input.readline().rstrip()
    directions = directions.replace("R", "1").replace("L", "0")
    input.readline()  # skip empty line

    for line in input:
        node, sides = line.rstrip().split(" = ")
        left, right = sides[1:-1].split(", ")
        map[node] = (left, right)

# PART 1


def part_1():
    start, end = "AAA", "ZZZ"
    left, right = 0, 1

    steps = 0
    current = start

    while current != end:
        for d in directions:
            if current == end:
                break
            steps += 1
            current = map[current][int(d)]

    print("Part #1: ", steps)


part_1()