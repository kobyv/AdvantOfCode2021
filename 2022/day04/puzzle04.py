# %% 1a

num_subsets = 0

with open("input.txt") as f:
    for line in f:
        r1, r2 = line.strip().split(",")
        r1_start, r1_end = [int(x) for x in r1.split("-")]
        r2_start, r2_end = [int(x) for x in r2.split("-")]

        if (r1_start <= r2_start and r1_end >= r2_end) or (
            r2_start <= r1_start and r2_end >= r1_end
        ):
            num_subsets += 1
print(num_subsets)

# %% 1b

num_subsets = 0

with open("input.txt") as f:
    for line in f:
        r1, r2 = line.strip().split(",")
        r1_start, r1_end = [int(x) for x in r1.split("-")]
        r2_start, r2_end = [int(x) for x in r2.split("-")]

        if (
            (r1_start <= r2_start <= r1_end)
            or (r1_start <= r2_end <= r1_end)
            or (r2_start <= r1_start <= r2_end)
            or (r2_start <= r1_end <= r2_end)
        ):
            num_subsets += 1
print(num_subsets)
