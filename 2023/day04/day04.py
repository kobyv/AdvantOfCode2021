test_input = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.splitlines()

with open('input.txt') as input:
    cards_sum = 0
    for card in input:
        card = card.rstrip()
        wnums, mnums = card.split(": ")[1].split(' | ')
        win_nums = set([int(n) for n in wnums.split(' ') if n])
        my_nums = set([int(n) for n in mnums.split(' ') if n])
        n = len(win_nums.intersection(my_nums)) 
        if n:
            cards_sum += 1 << (n-1)

    print(cards_sum)

# PART 2
with open('input.txt') as input:
    card_matches = []
    for card in input:
        card = card.rstrip()
        wnums, mnums = card.split(": ")[1].split(' | ')
        win_nums = set([int(n) for n in wnums.split(' ') if n])
        my_nums = set([int(n) for n in mnums.split(' ') if n])
        n = len(win_nums.intersection(my_nums))
        card_matches.append(n)

card_list = list(range(len(card_matches)))  # index of cards I have
num_cards = len(card_list)
i = 0
while i < len(card_list):
    card_index = card_list[i]
    n_matches = card_matches[card_index]
    card_list += list(range(card_index + 1, min(card_index + 1 + n_matches, num_cards)))
    i += 1

print('Part 2:', len(card_list))

