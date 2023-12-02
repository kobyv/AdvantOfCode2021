#!/usr/bin/env python3

input = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".splitlines()

maxred = 12
maxgreen = 13
maxblue = 14

good_games = []

with open("input.txt") as inp:
    for line in inp:
        game, data = line.rstrip().split(": ")
        gamenum = int(game.split(" ")[-1])
        sets = data.split("; ")
        game = []
        for s in sets:
            rgb = {"red": 0, "green": 0, "blue": 0}
            dice = s.split(", ")
            for d in dice:
                parts = d.split(" ")
                rgb[parts[1]] = int(parts[0])
            game.append(rgb)
        foul = [
            x
            for x in game
            if x["red"] > maxred or x["blue"] > maxblue or x["green"] > maxgreen
        ]
        if len(foul) == 0:
            good_games.append(gamenum)

    gamenum_sum = sum(good_games)

    print(gamenum_sum)

# Part 2

games = []

with open("input.txt") as input:
    for line in input:
        game, data = line.rstrip().split(": ")
        sets = data.split("; ")
        rgb = {"red": 1, "green": 1, "blue": 1}
        for s in sets:
            dice = s.split(", ")
            for d in dice:
                parts = d.split(" ")
                color = parts[1]
                num = int(parts[0])
                if num > rgb[color]:
                    rgb[color] = num

        power = rgb["red"] * rgb["blue"] * rgb["green"]
        games.append(power)

    game_sum = sum(games)
    print(game_sum)
