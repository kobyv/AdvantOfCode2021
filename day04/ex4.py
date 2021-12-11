import sys

bingo_list = []
bingo_cards = []
bingo_hits = []

def read_cards():
	global bingo_list, bingo_cards, bingo_hits
	with open('data.txt') as f:
		bingo_list = [int(x) for x in f.readline().split(',')]
		while True:
			spacer = f.readline()
			if not spacer: break
			card = []
			for i in range(5):
				q = [int(x) for x in f.readline().split()]
				assert(len(q) == 5)
				card += q
			bingo_cards.append(card)
			bingo_hits.append([False]*25)


def update_bingo_card(num, bingo_card, bingo_hit) -> bool:
	if not num in bingo_card:
		return False
	i = bingo_card.index(num)
	bingo_hit[i] = True
	#print(bingo_hit, '\n\n')
	for row in range(5):
		if all(bingo_hit[row*5:row*5+5]):
			#print('Row', row, bingo_card, bingo_hit)
			return True
	for col in range(5):
		if all(bingo_hit[col::5]):
			#print('Col', col, bingo_card, bingo_hit)
			return True
	return False

def calc_unmarked_numbers(bingo_card, bingo_hit) -> int:
	return sum(x[0] if not x[1] else 0 for x in zip(bingo_card, bingo_hit))

#
# MAIN
#

read_cards()
N = len(bingo_cards)
print('Number of cards:', N)

won_list = set([])

for num in bingo_list:
	#print('Number:', num)
	for card in range(N):
		#print('  Card:', card)
		if not card in won_list:
			won = update_bingo_card(num, bingo_cards[card], bingo_hits[card])
			if won:
				x = calc_unmarked_numbers(bingo_cards[card], bingo_hits[card])
				print('Result:', x*num)
				won_list.add(card)

print(won_list)