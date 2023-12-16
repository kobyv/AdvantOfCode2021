# %%
import numpy as np


def hash(word: str) -> int:
    sum = 0
    for c in word:
        sum += ord(c)
        sum *= 17
        sum %= 256
    return sum


def part1(filename: str):
    with open(filename) as input:
        data = input.read()

    data = data.replace("\n", "")  # in case of any newlines
    steps = data.split(",")

    total = 0
    for step in steps:
        total += hash(step)

    print("Day 15/ part1:", total)


#part1("input.txt")

def part2(filename: str):
    with open(filename) as input:
        data = input.read()

    data = data.replace("\n", "")  # in case of any newlines
    steps = data.split(",")

    boxes_name_list:  list[list[str]] = [[] for _ in range(256)]
    boxes_value_list: list[list[int]] = [[] for _ in range(256)]
    for step in steps:
        if step[-1] == '-':
            name = step[:-1]
            box = hash(name)
            if name not in boxes_name_list[box]:
                continue
            index = boxes_name_list[box].index(name)
            del boxes_name_list[box][index]
            del boxes_value_list[box][index]
        else:
            assert '=' in step
            name, val_str = step.split('=')
            val = int(val_str)
            box = hash(name)
            if name in boxes_name_list[box]:
                index = boxes_name_list[box].index(name) 
                boxes_value_list[box][index] = int(val)
            else:
                boxes_name_list[box].append(name)
                boxes_value_list[box].append(val)
    acc = 0
    for box in range(256):
        for i in range(len(boxes_name_list[box])):
            acc += (box + 1) * (i + 1) * boxes_value_list[box][i]
    return acc


print('PART 2:', part2('input.txt'))

# %%
