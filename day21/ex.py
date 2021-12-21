# %%
# We define the range as 0..9 instead of 1..10 (only in part 1)
# player_pos = [4 - 1, 8 - 1]  # test
player_pos = [3 - 1, 7 - 1]  # puzzle input
score = [0, 0]

dice_result = 6  # increases by 9 with each draw
current_player = 0

i = 0
while True:
    i += 3  # 3 dice rolls in each iteration
    new_pos = (player_pos[current_player] + dice_result) % 10
    player_pos[current_player] = new_pos
    dice_result += 9

    score[current_player] += new_pos + 1
    if score[current_player] >= 1000:
        break

    current_player = 1 - current_player

print("PART 1 result:", score[1 - current_player] * i)
# %%
# PART 2

options: dict[int, int] = {}  # count of each sum
for r1 in range(1, 4):
    for r2 in range(1, 4):
        for r3 in range(1, 4):
            options[r1 + r2 + r3] = options.get(r1 + r2 + r3, 0) + 1
assert sum(options.values()) == 27


def play(player, pos, multiplier, score, wins) -> None:
    """
    player: {0,1}
    pos: position vector
    wins: total number of wins per player
    """
    for cube_sum in options:
        how_many = options[cube_sum] * multiplier
        new_pos = pos[:]
        new_pos[player] = ((pos[player] + cube_sum - 1) % 10) + 1
        new_score = score[:]
        new_score[player] += new_pos[player]
        if new_score[player] >= 21:
            wins[player] += how_many
            continue
        play(1 - player, new_pos, how_many, new_score, wins)


# player_pos = [4, 8]  # test
player_pos = [3, 7]  # puzzle input
score = [0, 0]
wins = [0, 0]
play(0, player_pos, 1, score, wins)
print(wins)
print(max(wins))
# %%
