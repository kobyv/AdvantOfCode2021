# %% common

get_priority = (
    lambda r: ord(r) - ord("a") + 1 if "a" <= r <= "z" else ord(r) - ord("A") + 27
)

# %% 03a

sum_priorities = 0
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        assert len(line) % 2 == 0
        split_index = len(line) // 2
        left = line[:split_index]
        right = line[split_index:]
        for r in right:
            duplicate_item = ""
            if r in left:
                duplicate_item = r
                priority = get_priority(r)
                sum_priorities += priority
                break
print(sum_priorities)

# %% 03b

sum_priorities = 0
with open("demo_input.txt") as f:
    for elf1 in f:
        elf2 = next(f)
        elf3 = next(f)
        common = set(elf1.strip()).intersection(elf2.strip()).intersection(elf3.strip())
        assert len(common) == 1
        sum_priorities += get_priority(list(common)[0])
print(sum_priorities)
