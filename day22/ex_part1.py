import numpy as np

def read_file(fname) -> list[list[int]]:
    '''
    Each line returns as is_on,x1,x2,y1,y2,z1,z2
    '''
    with open(fname) as f:
        result = []
        for line in f:
            a = line.split(' ')
            assert(len(a) == 2)
            assert(a[0] in ('on','off'))
            is_on = (a[0] == 'on') + 0
            r: list[int] = [is_on] + [0] * 6
            b = a[1].split(',')  # each element looks like 'y=-20..30'
            for i,el in enumerate(b):
                assert(el[1] == '=')
                q = el[2:].split('..')
                r[i*2+1] = int(q[0])   # +1 because first element is is_on
                r[i*2+2] = int(q[1])
            result.append(r)
        return result

BASE = -50
SPAN = 101
b = np.zeros(SPAN**3, dtype=np.uint8)

def set_pixel(b, is_on, x, y, z):
    i = (z + BASE) + (y + BASE) * SPAN + (x + BASE) * SPAN*SPAN
    b[i] = is_on

def set_range(b, r: list[int]) -> None:
    '''
    range: same as each element returned by read_file()
    '''
    is_on, x1, x2, y1, y2, z1, z2 = r
    if x1 > -BASE or x2 < BASE or y1 > -BASE or y2 < BASE or z1 > -BASE or z2 < BASE:
        return
    x1 = max(x1, BASE)
    x2 = min(x2, -BASE)
    y1 = max(y1, BASE)
    y2 = min(y2, -BASE)
    z1 = max(z1, BASE)
    z2 = min(z2, -BASE)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                set_pixel(b, is_on, x, y, z)

def count_on_pixels(b):
    return np.sum(b)

inst = read_file('data.txt')
for line in inst:
    set_range(b, line)
print('PART 1 on cubes:', count_on_pixels(b))