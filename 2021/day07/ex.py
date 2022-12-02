# %%
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

#v = np.array([int(x) for x in '16,1,2,0,4,2,7,1,2,14'.split(',')])
v = np.array([int(x) for x in Path('data.txt').read_text().split(',')], dtype='int32')

v_set = set(v)

min_pos = -1
min_val = 100000000

for x in v_set:
	d = np.sum(np.abs(v - x))
	if d < min_val:
		min_val = d
		min_pos = x

print('# of elements:', len(v))
print('Min sum:', min_val)
print('pos:', min_pos)
# %%
# Problem B
def distance(d):
	return d*(d+1)/2

print('min:', np.min(v), 'max:', np.max(v))
q = np.zeros(np.max(v)+1, dtype='int32')
for x in range(np.max(v)+1):
	q[x] = np.sum(distance(np.abs(v - x)))
plt.plot(q)
print(min(q))
