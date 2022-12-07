from typing import Any

# keys: file names
# values: either sub-dict, or file size int
fs: dict[str, Any] = {}

# Current directory
path: list[str] = []


def display_file_system(fs, level=0):
    for f in fs:
        if isinstance(fs[f], int):
            print(f'{" "*level}{fs[f]} {f}')
        else:  # dir
            print(f'{" "*level}{f}:')
            display_file_system(fs[f], level + 1)


def find_dir(fs, path):
    for p in path:
        fs = fs[p]
    return fs


def handle_command(args: list[str]):
    if args[0] == "cd":
        if args[1] == "..":
            del path[-1]
        elif args[1] == "/":
            del path[:]
        else:
            path.append(args[1])
    elif args[0] == "ls":
        pass
    else:
        assert False


def handle_ls_output(args: list[str]):
    directory = find_dir(fs, path)
    if args[0] == "dir":
        directory[args[1]] = {}
    else:
        directory[args[1]] = int(args[0])  # value is file length


total_size = 0


def find_folders_of_at_most(fs, limit):
    size = 0
    for f in fs:
        if isinstance(fs[f], int):
            size += fs[f]
        else:
            size += find_folders_of_at_most(fs[f], limit)
    if size <= limit:
        global total_size
        total_size += size
    return size


with open("input.txt") as f:
    line = next(f).strip()
    assert line == "$ cd /"
    for line in f:
        args = line.strip().split()
        if args[0] == "$":
            handle_command(args[1:])
        else:
            handle_ls_output(args)

# display_file_system(fs)
total_size = 0
root_total_size = find_folders_of_at_most(fs, 100000)
print("\nPart 1 - Total size:", total_size)

# -- Part Two --

min_at_least = 1000000000


def find_folder_of_at_least(fs, limit):
    global min_at_least
    size = 0
    for f in fs:
        if isinstance(fs[f], int):
            size += fs[f]
        else:
            size += find_folder_of_at_least(fs[f], limit)
    if limit <= size < min_at_least:
        min_at_least = size
    return size


fs_size = 70000000
unused_space_at_least = 30000000
unused_size = fs_size - root_total_size
to_free_at_least = unused_space_at_least - unused_size

find_folder_of_at_least(fs, to_free_at_least)
print("Part 2 - Space to be freed:", min_at_least)
