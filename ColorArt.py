import datetime
import math
import random

import numpy as np
from PIL import Image


def split_list(l, last_n):
    return l[:-last_n], l[-last_n:]


def diff(c1, cs):
    [r1, g1, b1] = c1
    d = 0
    for c in cs:
        [r2, g2, b2] = c
        d += math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    d /= len(cs)

    # little modification to favor coordinates that have more neighbors
    d -= len(cs) / 1000.0
    return d


def next_coordinate(coors, poss_next, width):
    [item] = random.sample(poss_next, 1)
    poss_next.remove(item)

    row, col = item
    if 0 <= row < width - 1 and 0 <= col < width and coors[row + 1, col] == 0:
        poss_next.add((row + 1, col))
    if 1 <= row < width and 0 <= col < width and coors[row - 1, col] == 0:
        poss_next.add((row - 1, col))
    if 0 <= row < width and 0 <= col < width - 1 and coors[row, col + 1] == 0:
        poss_next.add((row, col + 1))
    if 0 <= row < width and 1 <= col < width and coors[row, col - 1] == 0:
        poss_next.add((row, col - 1))

    return row, col


def collect_neighbor_colors(row, col, neighbors, width, coors, picture):
    last_colors = []
    if 0 <= row < width - 1 and 0 <= col < width and coors[row + 1, col] == 1:
        last_colors.append(picture[row + 1, col])
    if 1 <= row < width and 0 <= col < width and coors[row - 1, col] == 1:
        last_colors.append(picture[row - 1, col])
    if 0 <= row < width and 0 <= col < width - 1 and coors[row, col + 1] == 1:
        last_colors.append(picture[row, col + 1])
    if 0 <= row < width and 1 <= col < width and coors[row, col - 1] == 1:
        last_colors.append(picture[row, col - 1])

    if neighbors == 8:
        if 0 <= row < width - 1 and 0 <= col < width - 1 and coors[row + 1, col + 1] == 1:
            last_colors.append(picture[row + 1, col + 1])
        if 1 <= row < width and 0 <= col < width - 1 and coors[row - 1, col + 1] == 1:
            last_colors.append(picture[row - 1, col + 1])
        if 0 <= row < width - 1 and 1 <= col < width and coors[row + 1, col - 1] == 1:
            last_colors.append(picture[row + 1, col - 1])
        if 1 <= row < width and 1 <= col < width and coors[row - 1, col - 1] == 1:
            last_colors.append(picture[row - 1, col - 1])

    return last_colors


def find_closest_color(temp_colors, last_colors):
    closest_diff = 10000000
    closest_color = None
    for color in temp_colors:
        temp_diff = diff(color, last_colors)
        if temp_diff < closest_diff:
            closest_color = color
            closest_diff = temp_diff
    return closest_color


def find_best_coordinate(coors, picture, neighbors, poss_next, color, width):
    closest_diff = 10000000

    best_coor = None
    for coor in poss_next:
        row, col = coor
        last_colors = collect_neighbor_colors(row, col, neighbors, width, coors, picture)
        temp_diff = diff(color, last_colors)
        if temp_diff < closest_diff:
            best_coor = coor
            closest_diff = temp_diff

    poss_next.remove(best_coor)

    row, col = best_coor
    if 0 <= row < width - 1 and 0 <= col < width and coors[row + 1, col] == 0:
        poss_next.add((row + 1, col))
    if 1 <= row < width and 0 <= col < width and coors[row - 1, col] == 0:
        poss_next.add((row - 1, col))
    if 0 <= row < width and 0 <= col < width - 1 and coors[row, col + 1] == 0:
        poss_next.add((row, col + 1))
    if 0 <= row < width and 1 <= col < width and coors[row, col - 1] == 0:
        poss_next.add((row, col - 1))

    if neighbors == 8:
        if 0 <= row < width - 1 and 0 <= col < width - 1 and coors[row + 1, col + 1] == 0:
            poss_next.add((row + 1, col + 1))
        if 1 <= row < width and 0 <= col < width - 1 and coors[row - 1, col + 1] == 0:
            poss_next.add((row - 1, col + 1))
        if 0 <= row < width - 1 and 1 <= col < width and coors[row + 1, col - 1] == 0:
            poss_next.add((row + 1, col - 1))
        if 1 <= row < width and 1 <= col < width and coors[row - 1, col - 1] == 0:
            poss_next.add((row - 1, col - 1))

    return best_coor


def main(dim=64, shuffle=True, colors_not_coors=True, neighbors=4):
    if dim not in [16, 64, 256]:
        print("Cannot create picture with the dimension specified.")
        return
    if not neighbors == 4 and not neighbors == 8:
        print("Number of neighbors can only be 4 or 8!")
        return

    width = int(math.pow(dim, 1.5))
    colors = list()
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                colors.append([i * 256 // dim, j * 256 // dim, k * 256 // dim])

    if shuffle:
        random.shuffle(colors)

    print('{:%X} All colors have been generated.'.format(datetime.datetime.now()))

    start = datetime.datetime.now()

    picture = np.zeros((width, width, 3), dtype=np.uint8)
    coors = np.zeros((width, width), dtype=np.uint8)
    poss_next = set([])

    if colors_not_coors:
        n_colors = 256

        temp_colors = colors[:n_colors]
        colors = colors[n_colors:]

        # color the first pixel randomly
        poss_next.add((random.randint(0, width - 1), random.randint(0, width - 1)))
        row, col = next_coordinate(coors, poss_next, width)
        coors[row, col] = 1
        picture[row, col, :] = temp_colors[-1]
        temp_colors.remove(temp_colors[-1])

        counter = 0
        while len(poss_next) > 0 and len(temp_colors) > 0:
            if (len(colors) + len(temp_colors)) % width == 0:
                img = Image.fromarray(picture)
                img.save('temp{:08d}.png'.format(counter))
                counter += 1
                now = datetime.datetime.now()
                time_left = ((now - start) / (width * width - len(colors))) * len(colors)
                print("{:%X} {} colors left to use, approximately {} left".format(datetime.datetime.now(),
                                                                                  len(colors) + len(temp_colors),
                                                                                  time_left))
            if len(colors) > 0:
                temp_colors.append(colors[-1])
                colors.pop()

            row, col = next_coordinate(coors, poss_next, width)
            coors[row, col] = 1

            last_colors = collect_neighbor_colors(row, col, neighbors, width, coors, picture)

            closest_color = find_closest_color(temp_colors, last_colors)

            temp_colors.remove(closest_color)
            picture[row, col, :] = closest_color

        img = Image.fromarray(picture)
        img.save('final_colors_{}_{}.png'.format(n_colors, dim))
        img.show()
    else:
        # color the first pixel randomly
        next_color = colors.pop()
        poss_next.add((random.randint(0, width - 1), random.randint(0, width - 1)))
        row, col = next_coordinate(coors, poss_next, width)
        coors[row, col] = 1
        picture[row, col, :] = next_color

        counter = 0
        while len(poss_next) > 0:
            if len(colors) % width == 0:
                img = Image.fromarray(picture)
                img.save('temp{:08d}.png'.format(counter))
                counter += 1
                now = datetime.datetime.now()
                if (width * width - len(colors)) != 0:
                    time_left = ((now - start) / (width * width - len(colors))) * len(colors)
                    print("{:%X} {} colors left to use, approximately {} left".format(datetime.datetime.now(),
                                                                                      len(colors),
                                                                                      time_left))

            next_color = colors.pop()
            row, col = find_best_coordinate(coors, picture, neighbors, poss_next, next_color, width)
            coors[row, col] = 1

            picture[row, col, :] = next_color

        img = Image.fromarray(picture)
        img.save('final_coors_{}.png'.format(dim))
        img.show()


main(dim=16, shuffle=False, colors_not_coors=False, neighbors=4)
