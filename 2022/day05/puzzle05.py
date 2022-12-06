import copy

containers = []
movements = (
    []
)  # movement insturctions: tuples or lists of (amount, from, to) using 1 based indexing
with open("input.txt") as f:
    # Read containers graphics
    for line in f:
        if line[1] == "1":
            break
        N = len(line)
        container_index = 0
        i = 1  # offset in line
        while i < N:
            if len(containers) <= container_index:
                containers.append([])
            if line[i] != " ":
                containers[container_index].insert(0, line[i])
            container_index += 1
            i += 4

    line = next(f)
    assert not line.strip()
    # Read move instructions
    for line in f:
        q = line.split()
        assert q[:5:2] == ["move", "from", "to"]
        m = [int(x) for x in q[1::2]]
        movements.append(m)

# print(containers)
# print(movements)

continers_copy = copy.deepcopy(containers)  # for part 2

# Perform the movements
for m in movements:
    (amount, from_idx, to_idx) = m
    for i in range(amount):
        x = containers[from_idx - 1][-1]
        del containers[from_idx - 1][-1]
        containers[to_idx - 1].append(x)

for c in containers:
    print(c)

result = "".join([c[-1] for c in containers])
print("Result:", result)

print("--- PART 2 ---")

containers = continers_copy
# Perform the movements
for m in movements:
    (amount, from_idx, to_idx) = m
    x = containers[from_idx - 1][-amount:]
    del containers[from_idx - 1][-amount:]
    containers[to_idx - 1].extend(x)

result = "".join([c[-1] for c in containers])
print("Result:", result)
