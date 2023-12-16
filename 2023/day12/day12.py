# %%

import numpy as np
from pathlib import Path

def parse_line(s: str) -> tuple[np.ndarray, list[int]]:
    '''Return an array of [0=operational, 1=broken, -1=unknown],
    and a list of broken spans
    '''
    broken_map_s, broken_list_s = s.split()
    broken_map_l = [{'?':-1,'.':0,'#':1}[x] for x in broken_map_s]
    broken_map = np.array(broken_map_l + [0], dtype=np.int8)
    broken_list = [int(x) for x in broken_list_s.split(',')]
    return broken_map, broken_list

def is_input_valid(b_map: np.ndarray, b_list: list[int]):
    N = len(b_map)
    i = 0
    for span in b_list:
        while i < N and b_map[i] == 0:
            i += 1
        if i == N:
            return False
        if b_map[i] == -1:
            return True
        j = i
        while i < N and b_map[i] == 1:
            i += 1
        if i < N and b_map[i] == -1:
            return True
        if i - j != span:
            return False
    return 1 not in b_map[i:]

def count_options_slow(b_map: np.ndarray, b_list: list[int], i: int=0) -> int:
    '''
    b_map, b_list: constants
    '''
    N = len(b_map)
    while i < N and b_map[i] != -1:
        i += 1
    is_valid = is_input_valid(b_map, b_list)
    if not is_valid:
        return 0
    if i == N:
        #if is_valid:
        #    print(b_map)
        return 1 if is_valid else 0
    count = 0
    map_0 = b_map.copy()
    map_0[i] = 0
    count += count_options_slow(map_0, b_list, i)
    map_1 = b_map.copy()
    map_1[i] = 1
    count += count_options_slow(map_1, b_list, i)
    return count

#print(count_options_slow(*parse_line('?###???????? 3,2,1')))

# %%

def count_options(b_map: np.ndarray, b_list: list[int], i: int, k: int) -> int:
    '''
    b_map: array per element: ?=-1, 0=., 1=#
    i: position in b_map
    k: position in b_list
    '''
    N = len(b_map)
    K = len(b_list)
    assert k < K
    limit = N - (sum(b_list[k:])+(K-k))
    count = 0
    #print(f'ENTER {i=}, {k=}, {limit=}')
    while i <= limit:
        while i <= limit and b_map[i] == 0:
            i += 1
        
        if i > limit:
            return count  # didn't use all spans
        
        # can we place a broken span?
        stop = i + b_list[k]
        if not (np.all(b_map[i:stop] != 0) and b_map[stop] != 1):
            # No, we can't
            if b_map[i] == 1:
                #print('RETURN, NO SPAN')
                return count  # imvalid arrangement, stop the search
        else:
            # Map {'?', '1'} -> '1'
            was = b_map.copy()  # FOR DEBUG
            b_map[i:stop] = 1  # FOR DEBUG
            b_map[stop] = 0  # FOR DEBUG
            if k == K-1:
                if np.any(b_map[stop+1:] == 1):
                    #print('RETURN, LAST SPAN, MORE #')
                    b_map = was  # FOR DEBUG
                    return count  # last span, but found '#' afterwards
                print(f'[SOLUTION!] {b_map=}')
                b_map = was
                count += 1
            else:  # not last span
                count += count_options(b_map, b_list, stop + 1, k+1)
                b_map = was  # FOR DEBUG
        if b_map[i] == 1:
            return count
        assert b_map[i] == -1, f'{i=}, {b_map[i]}, {b_map=}'  # and it must resolve to '.'
        # Map {'?'} -> '0' and continue
        b_map[i] = 0  # FOR DEBUG
        i += 1
        #print(f'CONTINUE {i=}, {k=}')
    return count

#print(count_options(*parse_line('?###???????? 3,2,1'), i=0, k=0))
#print(count_options(*parse_line('????.######..#####. 1,6,5'), i=0, k=0))

#b_map, b_list = parse_line('???.### 1,1,3')
#b_map, b_list = parse_line('.??..??...?##. 1,1,3')
#b_map, b_list = parse_line('?###???????? 3,2,1')
b_map, b_list = parse_line('???????.??? 1,3')
b_map[-1] = -1  # we added '.' anyways
b_map5 = np.concatenate((b_map, b_map, b_map, b_map, b_map))
b_list5 = b_list * 5
print(count_options(b_map5, b_list5, i=0, k=0))

# %%
count = 0
with open('input.txt') as f_in:
    for line in f_in:
        b_map, b_list = parse_line(line.strip())
        b_map[-1] = -1
        b_map5 = np.concatenate((b_map, b_map, b_map, b_map, b_map))
        b_list5 = b_list * 5
        c = count_options(b_map5, b_list5, i=0, k=0)
        print(f'{c=}')
        count += c
print(count)
# %%
