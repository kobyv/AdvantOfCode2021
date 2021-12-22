# %%
import numpy as np
from typing import Tuple

Pt = np.ndarray   # Point pseudo type having shape=(3,) and dtype=int32
Box = np.ndarray  # Box: shape=(6,) two points concatenated (x1,y1,z1,x2,y2,z2)

# We'll maintain a set of non-overlapping boxes representing on cubes.
# Each box holds a set of cubes and defined by p1=(x1,y1,z1),p2=(x2,y2,z2).
# p2 is exclusive (imagine real numbers).
# Adding a new "off" box B means that for any existing box A, we need to transform
# A into A' = A - B by possibly splitting it into multiple boxes.
#
# Adding a new "on" box B is the same, but after eliminating all overlapping regions,
# add the new box.
#
# So we need to implement a set difference operator

def diff_one_dimension(a1: int, a2: int, b1: int, b2: int):
    '''
    Perform A - B  on two 1-dimensional segments,
    where A is given by range (a1,a2) and B by (b1,b2).
    Return a tuple of:
    * First element: list of 0, one, or two segments that remain after diff operation
    * second element: the cut segment, or none if no overlap
    Each segment is given by 
    '''

    # Is there an overlap at all?
    if a1 >= b2 or b1 >= a2:
        return [(a1,a2)], None  # just return the original segment, no cut candidates

    # There is an overlap
    q1 = a1 >= b1
    q2 = a2 <= b2

    if q1 and q2:
        # A  |------|
        # B |---------|
        return [], (a1,a2)   # B covers A entirely
    if q2 and not q1:
        # A  |------|
        # B    |-----|
        return [(a1, b1)], (b1, a2)
    if q1 and not q2:
        # A   |-------|
        # B  |------|
        return [(b2, a2)], (a1, b2)
    if not q1 and not q2:
        # A |---------|
        # B  |------|
        return [(a1,b1), (b2,a2)], (b1,b2)
    assert(False)

def diff_3d(a: Box, b: Box) -> list[Box]:
    '''
    Perform A - B on boxes
    '''
    noncut_x, cut_x = diff_one_dimension(a[0],a[3],b[0],b[3])  # split dimension X
    noncut_y, cut_y = diff_one_dimension(a[1],a[4],b[1],b[4])
    noncut_z, cut_z = diff_one_dimension(a[2],a[5],b[2],b[5])
    if not cut_x or not cut_y or not cut_z: # at least one returned None?
        return [a]
    r: list[Box] = []  # result box set
    for x1,x2 in noncut_x:
        pt = np.array([x1,a[1],a[2],x2,a[4],a[5]])  # maintain Y,Z dims
        r.append(pt)
    for y1,y2 in noncut_y:
        pt = np.array([cut_x[0],y1,a[2],cut_x[1],y2,a[5]])
        r.append(pt) 
    for z1,z2 in noncut_z:
        pt = np.array([cut_x[0],cut_y[0],z1,cut_x[1],cut_y[1],z2])
        r.append(pt) 
    return r

def read_file(fname) -> list[list[int]]:
    """
    Each line returns as is_on,x1,x2,y1,y2,z1,z2
    """
    with open(fname) as f:
        result = []
        for line in f:
            a = line.split(" ")
            assert len(a) == 2
            assert a[0] in ("on", "off")
            is_on = (a[0] == "on") + 0
            r: list[int] = [is_on] + [0] * 6
            b = a[1].split(",")  # each element looks like 'y=-20..30'
            for i, el in enumerate(b):
                assert el[1] == "="
                q = el[2:].split("..")
                r[i * 2 + 1] = int(q[0])  # +1 because first element is is_on
                r[i * 2 + 2] = int(q[1])
            result.append(r)
        return result


def count_turned_on_cubes(boxes: list[Box]):
    acc = 0
    for b in boxes:
        acc += (b[3]-b[0])*(b[4]-b[1])*(b[5]-b[2])
    return acc


inst = read_file("data.txt")

boxes: list[Box] = []

for line in inst:
    is_on, x1, x2, y1, y2, z1, z2 = line
    newbox = np.array([x1, y1, z1, x2+1, y2+1, z2+1])
    r = []
    for b in boxes:
        chopped = diff_3d(b, newbox)
        r += chopped
    if is_on:
        r.append(newbox)  # after chopping all existing boxes with overlap, add the new one
    boxes = r

print(count_turned_on_cubes(boxes))
# %%
