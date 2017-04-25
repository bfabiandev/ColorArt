import math
import numpy as np
import scipy as sp
import random
from PIL import Image
import datetime



def diff(c1, cs):
    [r1, g1, b1] = c1
    d = 0
    for c in cs:
        [r2, g2, b2] = c
        d += math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return d


def next_coordinate(coors, poss_next, width):
    row, col = poss_next.pop()
    if 0 <= row < width - 1 and 0 <= col < width and coors[row + 1, col] == 0:
        poss_next.add((row + 1, col))
    if 1 <= row < width and 0 <= col < width and coors[row - 1, col] == 0:
        poss_next.add((row - 1, col))
    if 0 <= row < width and 0 <= col < width - 1 and coors[row, col + 1] == 0:
        poss_next.add((row, col + 1))
    if 0 <= row < width and 1 <= col < width and coors[row, col - 1] == 0:
        poss_next.add((row, col - 1))

    return row, col


dim = 64
width = int(math.pow(dim, 1.5))
colors = list()
for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            colors.append([i*256//dim, j*256//dim, k*256//dim])

random.shuffle(colors)

print('{:%X} All colors have been generated.'.format(datetime.datetime.now()))

picture = np.zeros((width, width, 3), dtype=np.uint8)
coors = np.zeros((width, width), dtype=np.uint8)
poss_next = set([])

nColors = 64

temp_colors = colors[:nColors]
colors = colors[nColors:]

# color the first pixel randomly
poss_next.add((random.randint(0, width), random.randint(0, width)))
row, col = next_coordinate(coors, poss_next, width)
coors[row, col] = 1
picture[row, col, :] = temp_colors[-1]
temp_colors.remove(temp_colors[-1])


counter = 0
while len(poss_next) > 0 and len(temp_colors) > 0:
    if (len(colors) + len(temp_colors)) % nColors == 0:
        img = Image.fromarray(picture)
        img.save('test{:08d}.png'.format(counter))
        counter += 1
        print("{:%X} {} colors left to use".format(datetime.datetime.now(), len(colors) + len(temp_colors)))

    if len(colors) > 0:
        temp_colors.append(colors[-1])
        colors.pop()

    row, col = next_coordinate(coors, poss_next, width)
    coors[row, col] = 1

    last_colors = list()

    if 0 <= row < width - 1 and 0 <= col < width and coors[row + 1, col] == 1:
        last_colors.append(picture[row + 1, col])
    if 1 <= row < width and 0 <= col < width and coors[row - 1, col] == 1:
        last_colors.append(picture[row - 1, col])
    if 0 <= row < width and 0 <= col < width - 1 and coors[row, col + 1] == 1:
        last_colors.append(picture[row, col + 1])
    if 0 <= row < width and 1 <= col < width and coors[row, col - 1] == 1:
        last_colors.append(picture[row, col - 1])

    closest_diff = 10000000
    closest_color = None
    for color in temp_colors:
        temp_diff = diff(color, last_colors)
        if temp_diff < closest_diff:
            closest_color = color
            closest_diff = temp_diff
    temp_colors.remove(closest_color)
    picture[row, col, :] = closest_color

img = Image.fromarray(picture)
img.save('test.png')
img.show()
