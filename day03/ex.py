N = 12
v = [0] * N
total = 0
with open('data.txt') as f:
	for line in f:
		line = line.strip()
		assert(len(line) == N)
		total += 1
		for i in range(len(line)):
			v[i] += int(line[i])

print('Total lines:', total)
result = ''.join(['1' if x >= total/2 else '0' for x in v])
print(result)

assert(not any([x == total/2 for x in v]))

r_int = int(result,2)
r_int_inv = (~r_int) & (2**N-1)

print(f'{r_int:012b}')
print(f'{r_int_inv:012b}')
print('Result:', r_int * r_int_inv)

print('** PART 2 **')
all_values = []
with open('data.txt') as f:
	for line in f:
		all_values.append(line.strip())

def solve(input_list, is_oxygen):
	v = input_list[:]
	for pos in range(N):
		cnt = 0
		for line in v:
			if line[pos] == '1':
				cnt += 1
		if is_oxygen:
			winner = '1' if cnt >= len(v)/2 else '0'
		else:
			winner = '1' if cnt < len(v)/2 else '0'

		#print('*'*(pos+1)+'V', winner)
		v = [line for line in v if line[pos] == winner]
		#print('\n'.join([x for x in v]))
		if len(v) == 1:
			return v[0]
		assert(len(v) > 0)

oxygen = solve(all_values, is_oxygen=True)
print('Oxygen:', oxygen)
co2 = solve(all_values, is_oxygen=False)
print('CO2:', co2)

oxygen_int = int(oxygen, 2)
co2_int = int(co2, 2)
print('Result:', oxygen_int * co2_int)
