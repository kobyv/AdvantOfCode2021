# %%
from typing import List, Sequence, Tuple, Union
import sys

TreeDS = Union[List[object], int]  # tree data structure
ListDS = List[int]  # list data structure containing OPENING and CLOSING

OPENING = -1
CLOSING = -2

def is_value(x: int) -> bool:
    return x >= 0

def magnitude(l: ListDS, pos: int) -> Tuple[int,int]:
    '''
    Return: (value, next pos to evaluate)
    '''
    l_value, pos = (l[pos], pos+1) if is_value(l[pos]) else magnitude(l, pos+1)
    if pos == len(l):
        return l_value, pos
    r_value, pos = (l[pos], pos+1) if is_value(l[pos]) else magnitude(l, pos+1)
    assert(l[pos] == CLOSING)
    pos += 1
    return (l_value * 3 + r_value * 2, pos)


def find_value(l: ListDS, pos: int, direction: int) -> int:
    '''
    Find next / previous value as given by direction (+1 or -1)
    Return position, or -1 if not found
    '''
    while 0 <= pos < len(l):
        if is_value(l[pos]):
            return pos
        pos += direction
    return -1

def tree_to_list0(e: TreeDS, l: ListDS) -> None:
    if isinstance(e, int):
        l.append(e)
    else:
        l.append(OPENING)
        assert(isinstance(e[0], list) or isinstance(e[0], int))
        assert(isinstance(e[1], list) or isinstance(e[1], int))
        tree_to_list0(e[0], l)
        tree_to_list0(e[1], l)
        l.append(CLOSING)

def tree_to_list(tree: TreeDS) -> ListDS:
    q: ListDS = []
    tree_to_list0(tree, q)
    return q

def tree2str(l: ListDS) -> str:
    s = ''
    for i,e in enumerate(l):
        if e == OPENING:
            if i > 0 and s[-1] != '[':
                s += ','
            s += '['
        elif e == CLOSING:
            s += ']'
        else:
            if i > 0 and s[-1] != '[':
                s += ','
            s += str(e)
    return s
            

def explode(l: ListDS) -> ListDS:
    nesting_level = 0
    for i,e in enumerate(l):
        if e == OPENING:
            nesting_level += 1
        elif e == CLOSING:
            nesting_level -= 1
        else:
            if nesting_level > 4:
                if i < len(l) - 1 and is_value(l[i+1]):  # two scalars?
                    # Let's explode
                    prevone = find_value(l, i-1, -1)
                    if prevone >= 0:
                        l[prevone] += e
                    nextone = find_value(l, i+3, 1)  # from pos: left, right, closing
                    if nextone >= 0:
                        l[nextone] += l[i+1]
                    return l[:i-1] + [0] + l[i+3:]   # OPENING POS(left) right CLOSING -> 0
    return l

def split(l: ListDS) -> ListDS:
    for i,e in enumerate(l):
        if e > 9:
            round_down = e // 2
            round_up = (e+1) // 2
            return l[:i] + [OPENING, round_down, round_up, CLOSING] + l[i+1:]
    return l

def reduce(l: ListDS) -> ListDS:
    while True:
        l0 = l
        l = explode(l)
        if l != l0:  # operation took place
            #print('Post explodum:', tree2str(l))
            continue
        l = split(l)
        if l != l0:  # operation took place
            #print('Post splitum:', tree2str(l))
            continue
        break
    return l

def add_all(l: List[ListDS]) -> ListDS:
    acc = l[0]
    for v in l[1:]:
        acc = reduce([OPENING] + acc + v + [CLOSING])
    return acc

def add_and_magnitude(x: ListDS, y: ListDS) -> int:
    return magnitude(reduce([OPENING] + x + y + [CLOSING]), 0)[0]

#homework = [[9,1],[1,9]]
# homework = [[[[[9,8],1],2],3],4]
# homework = [7,[6,[5,[4,[3,2]]]]]
# homework = [[6,[5,[4,[3,2]]]],1]
# homework = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
# homework = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# homework = [[[[0,7],4],[15,[0,13]]],[1,1]]
# homework = [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
# l: list[int] = []
# tree_to_list(homework, l)
# e = reduce(l)
# print(tree2str(e))

#(val, _) = magnitude(tree_to_list([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]), 0)
#assert(val == 3488)

print('** TEST **')

homework = '''\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

homework_list = [tree_to_list(eval(x.strip())) for x in homework.split('\n')]
e = add_all(homework_list)
print('\n', tree2str(e))
print('Magnitude:', magnitude(e, 0)[0])

print('** PART 1 **')
homework_list = []
with open('data.txt') as f:
    for line in f:
        homework_list.append(tree_to_list(eval(line.strip())))
e = add_all(homework_list)
print('\n', tree2str(e))
print('Magnitude:', magnitude(e, 0)[0])

print('** PART 2 **')
max_mag = -1
for i,x in enumerate(homework_list):
    for j,y in enumerate(homework_list):
        if i != j:
            m = add_and_magnitude(x, y)
            max_mag = max(max_mag, m)
print('Max magnitude:', max_mag)
