import itertools, math

def popcount(x: int) -> int:
	' number of binary 1 digits '
	return bin(x).count('1')

def log2_onehot(x: int) -> int:
	assert(x & (x-1) == 0)
	return int(math.log2(x))

def letters2bin(s: str) -> int:
	'abcdefg format to bitmap'
	r = 0
	s = s.strip()
	for c in s:
		v = ord(c) - ord('a')
		assert(0 <= v <= 9)
		r |= 1 << v
	return r

# PART 1

cnt = 0
with open('data.txt') as f:
	for line in f:
		alldigits_s, fourdigits_s = line.split('|')

		alldigits = [letters2bin(x) for x in alldigits_s.strip().split(' ')]
		fourdigits = [letters2bin(x) for x in fourdigits_s.strip().split(' ')]

		for d in fourdigits:
			if popcount(d) in (2, 3, 4, 7):  # digits 1, 7, 4, 8 respectively
				cnt += 1

print('Result PART 1:', cnt)

####################
# PART 2

correct_digits = (
    # 6543210
	0b1110111, # 0
	0b0100100, # 1
	0b1011101, # 2
	0b1101101, # 3
	0b0101110, # 4
	0b1101011, # 5
	0b1111011, # 6
	0b0100101, # 7
	0b1111111, # 8
	0b1101111  # 9
)

def permute(digit_in: int, p: list[int]) -> int:
	r = 0
	for i in range(7):
		if (digit_in >> p[i]) & 1:
			r |= 1 << i
	return r

def solve_permutation(alldigits: list[int]) -> list[int]:
	' returns the permutation of input wires to output wires '
	# Find digit 1 which has two LEDs
	digit1_value = [x for x in alldigits if popcount(x) == 2][0]
	# Find digits 7 which has one additional LED
	digit7_value = [x for x in alldigits if popcount(x) == 3][0]
	led0_src = log2_onehot(digit7_value & ~digit1_value)
	perm_base = set([0,1,2,3,4,5,6]).difference([led0_src])
	for p0 in itertools.permutations(perm_base):  # Which wire goes to which LED?
		p = [led0_src] + list(p0)
		for digit in alldigits:
			if not permute(digit, p) in correct_digits:
				break
		else:
			return p
	assert(False)

cnt = 0
with open('data.txt') as f:
	for line in f:
		alldigits_s, fourdigits_s = line.split('|')

		alldigits = [letters2bin(x) for x in alldigits_s.strip().split(' ')]
		fourdigits = [letters2bin(x) for x in fourdigits_s.strip().split(' ')]

		perm = solve_permutation(alldigits)
		num4digits = 0
		for digit in fourdigits:
			digit_perm = permute(digit, perm)
			i = correct_digits.index(digit_perm)
			num4digits = num4digits * 10 + i
		print(num4digits)
		cnt += num4digits

print('Result:', cnt)