import pathlib


def find_marker_index(s: str, n):
    i = n - 1
    while i < len(s):
        if len(set(s[i - (n - 1) : i + 1])) == n:
            print("Found at index", i + 1)
            return i + 1
        i += 1
    print("NOT FOUND")
    return 0


n = 4
assert find_marker_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", n) == 7
assert find_marker_index("bvwbjplbgvbhsrlpgdmjqwftvncz", n) == 5
assert find_marker_index("nppdvjthqldpwncqszvftbrmjlhg", n) == 6
assert find_marker_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", n) == 10
assert find_marker_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", n) == 11

s = pathlib.Path("input.txt").read_text()
print("PART 1 RESULT:")
find_marker_index(s, n)


n = 14
assert find_marker_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", n) == 19
assert find_marker_index("bvwbjplbgvbhsrlpgdmjqwftvncz", n) == 23

print("PART 2 RESULT:")
find_marker_index(s, n)
