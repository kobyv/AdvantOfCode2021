import sys

def check_cycle(cycle, x) -> int:
    if ((cycle - 20) % 40) == 0:
        #print(cycle, x, cycle*x)
        return cycle * x
    else:
        return 0

X = 1
total_strength = 0
cycle = 1

with open('input.txt') as f:
    for line in f:
        line = line.strip()
        #print(cycle, line)
        if line == 'noop':
            cycle += 1
            total_strength += check_cycle(cycle, X)
        else:
            (cmd, V) = line.split()
            assert cmd == 'addx'
            cycle += 1
            total_strength += check_cycle(cycle, X)
            cycle += 1
            X += int(V)
            #print(cycle, ' X = ', X)
            total_strength += check_cycle(cycle, X)

print('Strength:', total_strength)

# -- PART TWO --

def write(s): sys.stdout.write(s)

def screenify(cycle: int, X: int):
    crt_x = (cycle - 1) % 40  # zero indexed
    if crt_x == 0:
        write('\n')
    X -= 1
    write('#' if X <= crt_x <= X+2 else '.')

    

X = 1
cycle = 1

with open('input.txt') as f:
    for line in f:
        screenify(cycle, X)
        line = line.strip()
        if line == 'noop':
            cycle += 1
        else:
            (cmd, V) = line.split()
            assert cmd == 'addx'
            cycle += 1
            screenify(cycle, X)
            cycle += 1
            X += int(V)
screenify(cycle, X)
write('\n')

# Result should be: FCJAPJRE