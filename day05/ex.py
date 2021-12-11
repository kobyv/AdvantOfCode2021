#%%
from typing import Tuple

points: dict[Tuple[int,int],int] = {}

with open('data.txt') as f:
	for line in f:
		x1s,y1s,x2s,y2s = line.replace('->',',').split(',')
		x1,y1,x2,y2 = int(x1s), int(y1s), int(x2s), int(y2s)

		if y1==y2:
			for x in range(min(x1,x2),max(x1,x2)+1):
				points[(x,y1)] = points.get((x,y1),0) + 1
		elif x1==x2:
			for y in range(min(y1,y2), max(y1,y2)+1):
				points[(x1,y)] = points.get((x1,y),0) + 1

r = sum([1 for p in points if points[p] > 1])
print('Result:', r)

#%%
import sys
for y in range(10):
	for x in range(10):
		p = (x,y)
		sys.stdout.write(str(points.get(p,'.')))
	sys.stdout.write('\n')
# %%

#%%
points = {}
with open('data.txt') as f:
	for line in f:
		x1s,y1s,x2s,y2s = line.replace('->',',').split(',')
		x1,y1,x2,y2 = int(x1s), int(y1s), int(x2s), int(y2s)

		if y1==y2:
			for x in range(min(x1,x2),max(x1,x2)+1):
				points[(x,y1)] = points.get((x,y1),0) + 1
		elif x1==x2:
			for y in range(min(y1,y2), max(y1,y2)+1):
				points[(x1,y)] = points.get((x1,y),0) + 1
		else: # must be diagonal
			assert(abs(x2-x1) == abs(y2-y1))
			if x1 > x2:
				x1,x2 = x2,x1
				y1,y2 = y2,y1
			y_step = 1 if y2 > y1 else -1
			y = y1
			for x in range(x1,x2+1):
				points[(x,y)] = points.get((x,y), 0) + 1
				y += y_step


r = sum([1 for p in points if points[p] > 1])
print('Result:', r)

# %%
