# %%
from pathlib import Path

v_in = [int(v) for v in Path('data.txt').read_text().split(',')]
#v_in = [3,4,3,1,2]

population = [0] * 9

for v in v_in:
	population[v] += 1

for _ in range(256):  # 80 for first part
	zero = population[0]
	population = population[1:] + [0]
	population[6] += zero
	population[8] += zero

print(population)
print(sum(population))

# %%
