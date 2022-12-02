n0 = 100000000000000
cnt = 0
with open("input.txt") as f:
	for num_str in f:
		n = int(num_str)
		if n > n0:
			cnt += 1
		n0 = n
print(cnt)


# second ex
v = []
with open("input.txt") as f:
	for num_str in f:
		v.append(int(num_str))

cnt = 0
v_sum3 = []
n0 = 100000000000000
for i in range(len(v)-2):
	n = v[i] + v[i+1] + v[i+2]
	if n > n0:
		cnt += 1
	n0 = n
print(cnt)