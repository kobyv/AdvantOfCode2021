from typing import Dict

polymer_template: str = ""
instructions: Dict[str, str] = {}

with open("data.txt") as f:
    polymer_template = f.readline().rstrip()
    assert len(polymer_template) > 2
    f.readline()  # skip empty line

    for line in f:
        pair, insert = line.rstrip().split(" -> ")
        instructions[pair] = insert


def inc(d: Dict[str, int], el: str, howmuch: int = 1) -> None:
    d[el] = d.get(el, 0) + howmuch


el_freq: Dict[str, int] = {}  # element frequency
pair_freq: Dict[str, int] = {}  # element-pair frequency
for x in polymer_template:
    inc(el_freq, x)
for i in range(len(polymer_template) - 1):
    pair = polymer_template[i : i + 2]
    inc(pair_freq, pair)


def apply_iteration() -> None:
    "Update global el_freq, pair_freq"
    global pair_freq
    new_pair_freq: Dict[str, int] = {}
    for p in pair_freq:
        how_many = pair_freq[p]
        if not instructions[p]:
            new_pair_freq[p] = how_many
        else:
            new_el = instructions[p]
            inc(el_freq, new_el, how_many)
            new_pair1 = p[0] + new_el
            new_pair2 = new_el + p[1]
            inc(new_pair_freq, new_pair1, how_many)
            inc(new_pair_freq, new_pair2, how_many)
    pair_freq = new_pair_freq


for i in range(10):
    apply_iteration()

max_val = max(el_freq.values())
min_val = min(el_freq.values())
print("PART 1 Result:", max_val - min_val)

for i in range(30):  # 30 additional iterations (total 40)
    apply_iteration()

max_val = max(el_freq.values())
min_val = min(el_freq.values())
print("PART 2 Result:", max_val - min_val)
