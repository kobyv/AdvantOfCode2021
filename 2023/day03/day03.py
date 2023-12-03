import numpy as np
from pathlib import Path

def get_element(array, y, x) -> int:
    if x < 0 or x >= len(array[0]) or y < 0 or y >= len(array):
        return -1
    return array[y][x]

def update_set(d: set[int], idx_grid, y, x):
    index = get_element(idx_grid, y, x)
    if index < 1:  # 0=no number, -1=out of bounds
        return
    d.add(index)

def solve_1st_puzzle(in_grid: list[str]) -> int:
    N = len(in_grid[0].strip())
    # Step 1. generate an array that holds the whole number in
    #         each digit cell
    idx_grid: list[np.ndarray] = []  # each number has a unique index
    number_list: list[int] = [-1]
    for line in in_grid:
        line = line.strip()
        assert len(line) == N
        idx_line = np.zeros(N, dtype=np.uint32)
        is_searching = True
        current_number = 0
        starting_index = 1
        for i,c in enumerate(line+'.'):
            if is_searching:
                if not c.isdigit():
                    continue
                is_searching = False
                starting_index = i
            if not c.isdigit():
                idx_line[starting_index:i] = len(number_list)
                number_list.append(current_number)
                is_searching = True
                current_number = 0
                continue
            current_number = current_number * 10 + int(c)
        idx_grid.append(idx_line)
    
    # Step 2. compute the sum
    d: set[int] = set()  # set of global indices
    for y,line in enumerate(in_grid):
        for x,c in enumerate(line.strip()):
            if c.isdigit() or c == '.':
                continue
            # we found a symbol
            update_set(d, idx_grid, y-1, x-1)
            update_set(d, idx_grid, y-1, x+0)
            update_set(d, idx_grid, y-1, x+1)
            update_set(d, idx_grid, y+0, x-1)
            update_set(d, idx_grid, y+0, x+1)
            update_set(d, idx_grid, y+1, x-1)
            update_set(d, idx_grid, y+1, x+0)
            update_set(d, idx_grid, y+1, x+1)
    filtered_number_list = [number_list[i] for i in d]
    #print(filtered_number_list)
    return sum(filtered_number_list)

        

example_grid = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

#print(solve_1st_puzzle(example_grid.splitlines()))
print(solve_1st_puzzle(Path('input.txt').read_text().splitlines()))

def solve_2st_puzzle(in_grid: list[str]) -> int:
    N = len(in_grid[0].strip())
    # Step 1. generate an array that holds the whole number in
    #         each digit cell
    idx_grid: list[np.ndarray] = []  # each number has a unique index
    number_list: list[int] = [-1]
    for line in in_grid:
        line = line.strip()
        assert len(line) == N
        idx_line = np.zeros(N, dtype=np.uint32)
        is_searching = True
        current_number = 0
        starting_index = 1
        for i,c in enumerate(line+'.'):
            if is_searching:
                if not c.isdigit():
                    continue
                is_searching = False
                starting_index = i
            if not c.isdigit():
                idx_line[starting_index:i] = len(number_list)
                number_list.append(current_number)
                is_searching = True
                current_number = 0
                continue
            current_number = current_number * 10 + int(c)
        idx_grid.append(idx_line)
    
    # Step 2. compute the sum
    s = 0  # the sum
    for y,line in enumerate(in_grid):
        for x,c in enumerate(line.strip()):
            if c != '*':
                continue
            d: set[int] = set()  # set of global indices
            update_set(d, idx_grid, y-1, x-1)
            update_set(d, idx_grid, y-1, x+0)
            update_set(d, idx_grid, y-1, x+1)
            update_set(d, idx_grid, y+0, x-1)
            update_set(d, idx_grid, y+0, x+1)
            update_set(d, idx_grid, y+1, x-1)
            update_set(d, idx_grid, y+1, x+0)
            update_set(d, idx_grid, y+1, x+1)
            if len(d) == 2:
                s += np.prod(np.array(number_list)[list(d)])
    return s

print('Part 2\n======')
#print(solve_2st_puzzle(example_grid.splitlines()))
print(solve_2st_puzzle(Path('input.txt').read_text().splitlines()))
