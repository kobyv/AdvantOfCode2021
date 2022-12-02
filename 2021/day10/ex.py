from typing import Tuple

penalties = {")": 3, "]": 57, "}": 1197, ">": 25137}


def process_string(s: str) -> Tuple[int, str]:
    "returns a tuple of points (part 1) and closing order (part 2)"
    bracket_options = "()[]{}<>"
    stack: list[str] = []  # characters stack
    for c in s:
        assert c in bracket_options
        if c in "([{<":
            matching_bracket = bracket_options[bracket_options.index(c) + 1]
            stack.append(matching_bracket)
            continue
        # closing bracket
        if len(stack) == 0 or c != stack[-1]:
            return (penalties[c], "")
        stack = stack[:-1]
    return (0, "".join(stack[::-1]))  # success


print("PART 1")

points_sum = 0
with open("data.txt") as f:
    for line in f:
        (points, _) = process_string(line.strip())
        points_sum += points
print(points_sum)

print("PART 2")

closing_points = {")": 1, "]": 2, "}": 3, ">": 4}

def calc_closing_score(s: str) -> int:
    score = 0
    for c in s:
        score = score * 5 + closing_points[c]
    return score

score_list: list[int] = []

with open("data.txt") as f:
    for line in f:
        (_, closing) = process_string(line.strip())
        if closing:
            score_list.append(calc_closing_score(closing))
assert(len(score_list) & 1 == 1)

print(sorted(score_list)[len(score_list)//2])