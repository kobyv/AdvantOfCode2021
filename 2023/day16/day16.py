# %%

import numpy as np
from enum import IntEnum
from pathlib import Path


class Type(IntEnum):
    EMPTY = 0
    SPLIT_V = 1
    SPLIT_H = 2
    FSLASH = 3  # forward slash
    BSLASH = 4  # backward slack


class Dir(IntEnum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


FSLASH_DIR = [0] * 4
FSLASH_DIR[Dir.UP] = Dir.RIGHT
FSLASH_DIR[Dir.RIGHT] = Dir.UP
FSLASH_DIR[Dir.LEFT] = Dir.DOWN
FSLASH_DIR[Dir.DOWN] = Dir.LEFT

BSLASH_DIR = [0] * 4
BSLASH_DIR[Dir.UP] = Dir.LEFT
BSLASH_DIR[Dir.RIGHT] = Dir.DOWN
BSLASH_DIR[Dir.LEFT] = Dir.UP
BSLASH_DIR[Dir.DOWN] = Dir.RIGHT

Cave = np.ndarray
WasHere = np.ndarray  # Per cell, all directions light traveled


def move(y: int, x: int, d: Dir) -> tuple[int, int]:
    "Move one step in given direction"
    match d:
        case Dir.UP:
            y -= 1
        case Dir.DOWN:
            y += 1
        case Dir.LEFT:
            x -= 1
        case Dir.RIGHT:
            x += 1
    return (y, x)


def travel(c: Cave, wh: WasHere, y: int, x: int, d: Dir) -> None:
    Y, X = c.shape
    def is_outside(y, x):
        return x < 0 or x >= X or y < 0 or y >= Y
    while True:
        if wh[y, x] & (1 << d) != 0:
            return
        _wh = wh[y,x]
        wh[y, x] |= 1 << d
        #print(y,x,d)
        match c[y, x]:
            case Type.EMPTY:
                pass
            case Type.FSLASH:
                d = Dir(FSLASH_DIR[int(d)])
                #print(y,x,d)
            case Type.BSLASH:
                d = Dir(BSLASH_DIR[int(d)])
                #print(y,x,d)
            case Type.SPLIT_V:
                if _wh & ((1 << Dir.LEFT) | (1 << Dir.RIGHT)):
                    return
                if d in (Dir.LEFT, Dir.RIGHT):
                    y1 = y - 1
                    x1 = x
                    if not is_outside(y1, x1):
                        #print(y1,x1,Dir.UP, 'ENTER')
                        travel(c, wh, y1, x1, Dir.UP)
                    d = Dir.DOWN
                    #print(y,x,d, 'LEAVE')
            case Type.SPLIT_H:
                if _wh & ((1 << Dir.UP) | (1 << Dir.DOWN)):
                    return
                if d in (Dir.UP, Dir.DOWN):
                    y1 = y
                    x1 = x - 1
                    if not is_outside(y1, x1):
                        #print(y1,x1,Dir.LEFT, 'ENTER')
                        travel(c, wh, y1, x1, Dir.LEFT)
                    d = Dir.RIGHT
                    #print(y,x,d, 'LEAVE')
        y, x = move(y, x, d)
        if is_outside(y, x):
            return



def read_cave(s: str) -> Cave:
    m = {
        ".": Type.EMPTY,
        "|": Type.SPLIT_V,
        "-": Type.SPLIT_H,
        "/": Type.FSLASH,
        "\\": Type.BSLASH,
    }
    z = []
    for line in s.splitlines():
        line_list = [m[c] for c in line.strip()]
        z.append(line_list)
    return np.array(z, dtype=np.uint8)

def draw_cave(c: Cave, wh: WasHere):
    Y, X = c.shape
    with open('cave.html', 'w') as f:
        f.write('<code>\n')
        for y in range(Y):
            for x in range(X):
                if wh[y,x] != 0:
                    f.write('<span style="color:red">')
                match c[y,x]:
                    case Type.EMPTY:
                        f.write('.')
                    case Type.SPLIT_V:
                        f.write('|')
                    case Type.SPLIT_H:
                        f.write('-')
                    case Type.FSLASH:
                        f.write('/')
                    case Type.BSLASH:
                        f.write('\\')
                if wh[y,x] != 0:
                    f.write('</span>')
            f.write('<br>\n')
        f.write('</code>\n')

def score(wh: WasHere):
    return (wh != 0).flatten().sum()

def part2_find_max(c: Cave) -> int:
    Y, X = c.shape
    max_score = 0

    # Top, bottom rows
    for x in range(X):
        wh = np.zeros(c.shape, dtype=np.uint8)
        travel(c, wh, 0, x, Dir.DOWN)
        max_score = max(max_score, score(wh))
        wh = np.zeros(c.shape, dtype=np.uint8)
        travel(c, wh, Y-1, x, Dir.UP)
        max_score = max(max_score, score(wh))
    # Left, right cols
    for y in range(Y):
        wh = np.zeros(c.shape, dtype=np.uint8)
        travel(c, wh, y, 0, Dir.RIGHT)
        max_score = max(max_score, score(wh))
        wh = np.zeros(c.shape, dtype=np.uint8)
        travel(c, wh, y, X-1, Dir.LEFT)
        max_score = max(max_score, score(wh))
    return max_score    


example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

if False:
    c = read_cave(example)
    wh = np.zeros(c.shape, dtype=np.uint8)

    travel(c, wh, 0, 0, Dir.RIGHT)
    print(score(wh))
    #draw_cave(c, wh)
    print('MAX score:', part2_find_max(c))

c = read_cave(Path('input.txt').read_text())
wh = np.zeros(c.shape, dtype=np.uint8)
travel(c, wh, 0, 0, Dir.RIGHT)
print('PART 1:', (wh != 0).flatten().sum())
#draw_cave(c, wh)

# PART 2
print('PART 2:', part2_find_max(c))

# %%
