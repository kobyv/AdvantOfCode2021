x = 0
y = 0
with open('data.txt') as f:
	for line in f:
		dir, howmuch_str = line.split()
		howmuch = int(howmuch_str)
		if dir == 'forward':
			x += howmuch
		elif dir == 'down':
			y += howmuch
		elif dir == 'up':
			y -= howmuch
		else:
			assert(False)

print(x,y)
print(x*y)

print('Second part')
x = 0
depth = 0
aim = 0
with open('data.txt') as f:
	for line in f:
		dir, howmuch_str = line.split()
		howmuch = int(howmuch_str)
		if dir == 'forward':
			x += howmuch
			depth += aim * howmuch
		elif dir == 'down':
			aim += howmuch
		elif dir == 'up':
			aim -= howmuch
		else:
			assert(False)
print(x,depth)
print(x*depth)