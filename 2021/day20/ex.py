from typing import Tuple


def read_file(fname: str, frame_size: int) -> Tuple[list[str], str]:
    with open(fname) as f:
        kernel = f.readline().strip()
        assert len(kernel) == 512
        assert not f.readline().strip()  # spacer line
        image: list[str] = []
        for line in f:
            image.append(
                "." * frame_size + line.strip() + "." * frame_size
            )  # Take care of column edges
        N = len(image[0])
        image = ["." * N] * frame_size + image + ["." * N] * frame_size
        assert len(image) == N
    return (image, kernel)


def convolve(image: list[str], kernel: str) -> list[str]:
    N = len(image)
    r = [l[:] for l in image]  # image copy by value
    assert kernel[0] == "#" and kernel[511] == "."
    boundary = "#" if image[0][0] == "." else "."
    for y in range(1, N - 1):
        r[y] = boundary + r[y][1 : N - 1] + boundary
        for x in range(1, N - 1):
            s = (
                image[y - 1][x - 1 : x + 2]
                + image[y][x - 1 : x + 2]
                + image[y + 1][x - 1 : x + 2]
            )
            b = int(s.replace("#", "1").replace(".", "0"), 2)
            # strings are immutable
            line = r[y]
            r[y] = line[:x] + kernel[b] + line[x + 1 :]
            assert len(image[y]) == N
    # Take care of the boundary which should be inverted
    r[0] = boundary * N
    r[N - 1] = boundary * N

    return r


def count_lit_pixels(image: list[str]) -> int:
    cnt = 0
    for line in image:
        cnt += sum([1 if x == "#" else 0 for x in line])
    return cnt


#
# MAIN
#

# The kernel is weird. If all 9 pixels are not lit, the result is lit (all the infinite world).
image, kernel = read_file("data.txt", 52)  # 52 due to part 2

r = convolve(convolve(image, kernel), kernel)
print("PART 1 lit pixels:", count_lit_pixels(r))

# PART 2
r = image
for i in range(50):
    r = convolve(r, kernel)
print("PART 2 lit pixels:", count_lit_pixels(r))

# for i in r: print(i)
