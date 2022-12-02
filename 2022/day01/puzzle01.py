# 1a

max_sum = 0
current_sum = 0

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            current_sum += int(line)
        else:
            if current_sum > max_sum:
                max_sum = current_sum
            current_sum = 0

print(max_sum)

# 1b
print("** 1b **")
sums_table = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            current_sum += int(line)
        else:
            sums_table.append(current_sum)
            current_sum = 0
sums_table = sorted(sums_table, reverse=True)
print(sum(sums_table[:3]))
