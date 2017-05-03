import datetime
import math
import random

import numpy as np
from PIL import Image


def diff(c1, cs):
    [r1, g1, b1] = c1.astype(int)
    d = 0
    for c in cs:
        [r2, g2, b2] = c.astype(int)
        d += math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return d


dim = 64
width = int(math.pow(dim, 1.5))
colors = list()
for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            colors.append([i * 256 // dim, j * 256 // dim, k * 256 // dim])

random.shuffle(colors)

picture = np.asarray(colors, dtype=np.uint8).reshape((width, width, 3))

print('{:%X} All colors have been generated.'.format(datetime.datetime.now()))

n_of_switches = 1000000

for i in range(n_of_switches):
    if i % 100000 == 0:
        img = Image.fromarray(picture)
        img.save('test{:08d}.png'.format(i))
        print("{:%X} {}".format(datetime.datetime.now(), i))

    row_start = random.randint(0, width - 1)
    col_start = random.randint(0, width - 1)
    row_end = random.randint(0, width - 1)
    col_end = random.randint(0, width - 1)

    if row_start == row_end and col_start == col_end:
        continue

    color_start = picture[row_start, col_start, :]
    color_end = picture[row_end, col_end, :]

    last_colors_start = []
    last_colors_end = []

    if 0 <= row_start < width - 1 and 0 <= col_start < width:
        last_colors_start.append(picture[row_start + 1, col_start])
    if 1 <= row_start < width and 0 <= col_start < width:
        last_colors_start.append(picture[row_start - 1, col_start])
    if 0 <= row_start < width and 0 <= col_start < width - 1:
        last_colors_start.append(picture[row_start, col_start + 1])
    if 0 <= row_start < width and 1 <= col_start < width:
        last_colors_start.append(picture[row_start, col_start - 1])

    if 0 <= row_end < width - 1 and 0 <= col_end < width:
        last_colors_end.append(picture[row_end + 1, col_end])
    if 1 <= row_end < width and 0 <= col_end < width:
        last_colors_end.append(picture[row_end - 1, col_end])
    if 0 <= row_end < width and 0 <= col_end < width - 1:
        last_colors_end.append(picture[row_end, col_end + 1])
    if 0 <= row_end < width and 1 <= col_end < width:
        last_colors_end.append(picture[row_end, col_end - 1])

    diff_start = diff(color_start, last_colors_start)
    diff_end = diff(color_end, last_colors_end)
    new_diff_start = diff(color_start, last_colors_end)
    new_diff_end = diff(color_end, last_colors_start)

    if (diff_start + diff_end) > (new_diff_start + new_diff_end):
        picture[row_start, col_start, :] = color_end[:]
        picture[row_end, col_end, :] = color_start[:]

img = Image.fromarray(picture)
img.save('test{:08d}.png'.format(n_of_switches))
img.show()
