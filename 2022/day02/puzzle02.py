# Index   What?             Value
#     0   Rock      A   X   1
#     1   Paper     B   Y   2
#     2   Scissors  C   Z   3

# Score: 0=loose, 3=draw, 6=win

# %% 1a

total_score = 0

with open("input.txt") as f:
    for line in f:
        s = line.strip().split()
        opponent = ord(s[0]) - ord("A")
        my = ord(s[1]) - ord("X")
        d = (my - opponent + 3) % 3  # 0=draw, 1=win, 2=loose
        total_score += my + 1
        if d == 0:  # draw
            total_score += 3
        elif d == 1:
            total_score += 6

print(total_score)

# %% 1b

total_score = 0

with open("input.txt") as f:
    for line in f:
        s = line.strip().split()
        opponent = ord(s[0]) - ord("A")
        d = {"X": 2, "Y": 0, "Z": 1}[s[1]]
        my = (d + opponent + 3) % 3
        total_score += my + 1
        if d == 0:  # draw
            total_score += 3
        elif d == 1:
            total_score += 6

print(total_score)
