h: list[list[int]] = []

with open("data.txt") as f:
    for line in f:
        h.append([10] + [int(x) for x in line.strip()] + [10])

Nx = len(h[0])

h = [[10] * Nx] + h + [[10] * Nx]
Ny = len(h)
s = 0

for y in range(1, Ny - 1):
    for x in range(1, Nx - 1):
        if (
            h[y][x] < h[y - 1][x]
            and h[y][x] < h[y + 1][x]
            and h[y][x] < h[y][x + 1]
            and h[y][x] < h[y][x - 1]
        ):
            s += h[y][x] + 1

print('Part 1 sum:', s)

####################
# PART 2

# Flood fill areas
print("PART 2")

num_ponds = 0
pond_index = [[False] * Nx for _ in range(Ny)]  # Whether in pond

def floodfill(x:int,y:int, num_elements:int) -> int:
    if h[y][x] >= 9:
        return num_elements
    if pond_index[y][x]:
        return num_elements
    num_elements += 1
    pond_index[y][x] = True
    num_elements = floodfill(x+1, y, num_elements)
    num_elements = floodfill(x-1, y, num_elements)
    num_elements = floodfill(x, y+1, num_elements)
    num_elements = floodfill(x, y-1, num_elements)
    return num_elements

pond_sizes: list[int] = []

for y in range(1,Ny-1):
    for x in range(1, Nx-1):
        num_elements = floodfill(x,y,0)
        if num_elements > 0:
            #print('Pond size:', num_elements)
            pond_sizes.append(num_elements)

pond_sizes.sort(reverse=True)
print('Part 2 result:', pond_sizes[0]*pond_sizes[1]*pond_sizes[2])
