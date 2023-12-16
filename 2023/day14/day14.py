#!/usr/bin/env python3

# %% 
import numpy as np

ROUND = 2
CUBE = 1
EMPTY = 0

def mat2display(mat: np.ndarray) -> str:
    res = ''
    imat = mat.tolist()

    for l in imat:
        line = ''
        for n in l:
            if n == ROUND:
                line = line + 'O'
            elif n == CUBE:
                line = line + '#'
            elif n == EMPTY:
                line = line + '.'
            else:
                assert(f'Incorrect value detected: {n}')
        line = line + '\n'
        res = res + line
    res = res + '\n'    
    return res


def inp2int(inp: list[str]) -> list[list[int]]:
    res = []
    for line in inp:
        iline = []
        line = line.rstrip()
        for c in line:
            if c == 'O':
                iline.append(ROUND)
            elif c == '#':
                iline.append(CUBE)
            else:
                iline.append(EMPTY)        
        res.append(iline)
    return res


def inp2matrix(inp: list[str]) -> np.ndarray:
    nparr = np.array(inp2int(inp), dtype=np.int32)
    return nparr


def shakeit(platorig: np.ndarray) -> np.ndarray:
    plat = platorig.copy()

    numlines = plat.shape[0]
    numcols = plat.shape[1]
    # weight = numlines - i
    
    for col in range(numcols):
        rline = 0
        wline = 0 
        while rline < numlines: 
            if plat[rline][col] == ROUND:
                plat[rline][col] = EMPTY
                plat[wline][col] = ROUND
                rline += 1
                wline += 1
            elif plat[rline][col] == CUBE:
                rline +=1
                wline = rline
            else:
                rline += 1
    return plat

def cycle(plat: np.ndarray) -> (np.ndarray, bool):
    orig = plat
    plat = shakeit(plat) # N
    plat = plat.T
    plat = np.flip(plat,axis=1) # turn clockwise
    plat = shakeit(plat) # W
    plat = plat.T
    plat = np.flip(plat,axis=1) # turn clockwise
    plat = shakeit(plat) # S
    plat = plat.T
    plat = np.flip(plat,axis=1) # turn clockwise
    plat = shakeit(plat) # E
    plat = plat.T
    plat = np.flip(plat,axis=1) # turn clockwise

    return plat, np.array_equal(orig, plat)


def summarize_weights(plat: np.ndarray) -> int:
    numlines = plat.shape[0]
    numcols = plat.shape[1]
    sum = 0
    for x in range(0, numlines):
        factor = numlines - x
        for y in range(0, numcols):
            if plat[x][y] == ROUND:
                sum += factor 
    return sum

def part1():
    with open('input.txt') as input:
        inp = input.readlines()
        platform = inp2matrix(inp)
        numlines = platform.shape[0]
        numcols = platform.shape[1]
        print(mat2display(platform))

        platform = shakeit(platform)

        print(mat2display(platform))                    
                    
        sum = 0

        for x in range(0, numlines):
            factor = numlines - x
            for y in range(0, numcols):
                if platform[x][y] == ROUND:
                    sum += factor 

        print("day 14, part 1: ", sum)            

def find_in_mem(modmem: list[np.ndarray], item: np.ndarray) -> int:
    for i in range(len(modmem)):
        if modmem[i] is not None and np.array_equal(modmem[i], item):
            return i
    return -1        



def part2():
    maxcycles = 1000000000

    modmem = [None] * 1000

    with open('input.txt') as input:
        inp = input.readlines()
        platform = inp2matrix(inp)
        print("Before...")
        print(mat2display(platform), '\n') 


        for i in range(maxcycles):
            platform, isit = cycle(platform)
            if i % 100000 == 0:
                print(i)    
            if isit:
                print(i, "Identical!")    
                break
            else:
                found = find_in_mem(modmem, platform)
                sum = summarize_weights(platform)                
                if found > 0:
                    print(f'{i=}, {found=}, {sum=}')
                    if i > 1000:
                        break
                else:
                    modmem[i % 1000] = platform

        #print("Day 14, part 2:", sum)

part2()

# %%
#
# Found a cycle of 102. Take a base like i=802 (lowest found=88)
# and take sum of i=((1_000_000_000-802) % 102 + 802)
    
