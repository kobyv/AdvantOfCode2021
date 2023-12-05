from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Range:
    src: int  # starting index
    cnt: int


@dataclass(frozen=True, slots=True, order=True)
class Translate:
    src: int  # starting index
    cnt: int
    dst: int  # src+i -> dst+i


def intersect_translate(x: Range, y: Translate) -> Range:
    start = max(x.src, y.src)
    end = min(x.src + x.cnt, y.src + y.cnt)
    return Range(y.dst + start - y.src, max(end - start, 0))


def intersect_translate_list(
    x_list: list[Range], y_list: list[Translate]
) -> list[Range]:
    """
    Intersect and translate incoming range x with y_list (y_list must be gaps extended),
    y_list must be sorted and gaps extended
    """
    r: list[Range] = []
    for x in x_list:
        for y in y_list:
            q = intersect_translate(x, y)
            if q.cnt:
                r.append(q)
    return r


LARGE_INT = 10**16


def extend_translations_with_gaps(t: list[Translate]) -> list[Translate]:
    t = sorted(t)
    r = []
    r.append(Translate(-LARGE_INT, t[0].src + LARGE_INT, -LARGE_INT))
    for i in range(len(t) - 1):
        r.append(t[i])
        gap_start = t[i].src + t[i].cnt
        gap_end = t[i + 1].src
        assert gap_end >= gap_start, f"{gap_end}, {gap_start}"
        if gap_end > gap_start:
            r.append(Translate(gap_start, gap_end - gap_start, gap_start))
    r.append(t[-1])
    gap_start = t[-1].src + t[-1].cnt
    r.append(Translate(gap_start, LARGE_INT - gap_start, gap_start))
    return r


translations: list[list[Translate]] = []


# For part 1: the easy solution
def translate(x: int):
    for layer in translations:
        for t in layer:
            if x >= t.src and x < t.src + t.cnt:
                x = t.dst + x - t.src
                break
    return x


input_txt = Path("input.txt").read_text().splitlines()

assert input_txt[0].startswith("seeds: ")
seeds = [int(v) for v in input_txt[0][7:].split(" ")]

i = 2
while i < len(input_txt):
    # print(i, input_txt[i])
    assert input_txt[i].strip()[-1] == ":"
    i += 1
    l: list[Translate] = []  # dst, src, cnt  translation mapping
    while i < len(input_txt):
        if not input_txt[i].strip():
            i += 1
            break
        dst, src, cnt = [int(v) for v in input_txt[i].split(" ")]
        # print(dst, src, cnt)
        l.append(Translate(src, cnt, dst))
        i += 1
    translations.append(l)


seeds_translated = [translate(x) for x in seeds]
print(min(seeds_translated))


print("\n\n--- Part Two ---")
translations = [extend_translations_with_gaps(t) for t in translations]

assert len(seeds) % 2 == 0
min_found = LARGE_INT
for i in range(len(seeds) // 2):
    x = [Range(seeds[i * 2], seeds[i * 2 + 1])]
    for t in translations:
        x = intersect_translate_list(x, t)
    min_in_range = min([q.src for q in x])
    min_found = min(min_found, min_in_range)

print("Min seed:", min_found)
