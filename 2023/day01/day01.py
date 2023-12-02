#!/usr/bin/env python3

input = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".splitlines()


with open("input.txt") as inp:
    sum = 0
    for line in inp:
        digits = []
        for c in line:
            if c.isdigit():
                digits.append(c)
        sum += int(f"{digits[0]}{digits[-1]}")

    print("Result 1:", sum)

input2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".splitlines()

words = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
sum = 0

with open("input.txt") as input2:
    for line in input2:
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(c)
            else:
                for word in words.keys():
                    if line[i:].startswith(word):
                        digits.append(words[word])
        sum += int(f"{digits[0]}{digits[-1]}")

print("Result 2:", sum)
