import math
import numpy as np
import random
from PIL import Image

import fractal_dep as dp

def fill_in_square(top_l, top_r, bott_l, bott_r, colour, pixels):
    corners = [top_l, top_r, bott_r, bott_l]
    min_x = max(0, int(min(p[0] for p in corners)))
    max_x = min(len(pixels) - 1, int(max(p[0] for p in corners)))
    min_y = max(0, int(min(p[1] for p in corners)))
    max_y = min(len(pixels[0]) - 1, int(max(p[1] for p in corners)))
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            inside = False
            j = len(corners) - 1
            for i in range(len(corners)):
                x1, y1 = corners[i]
                xj, yj = corners[j]
                if ((y1 > y) != (yj > y)):
                    intersection_x = (
                        (xj - x1) * (y-y1) / (yj-y1) + x1
                    )
                    if x < intersection_x:
                        inside = not inside
                j = i
            if inside:
                if np.array_equal(pixels[x][y], (0, 0, 0)):
                    pixels[x][y] = colour



def plot_line(cord1, cord2, thickness, colour, pixels):
    mXCord = len(pixels[0])
    mYCord = len(pixels)
    h_dis = cord2[0] - cord1[0]
    v_dis = cord2[1] - cord1[1]
    distance = math.sqrt(h_dis ** 2 + v_dis ** 2)
    h_step = h_dis / distance
    v_step = v_dis / distance
    for i in range(round(distance)):
        cXCord = round(cord1[0] + (h_step * i))
        cYCord = round(cord1[1] + (v_step * i))

        for x in range (-thickness, thickness):
            for y in range(-thickness, thickness):
                x_val = cXCord + x
                y_val = cYCord + y
                if (x_val > 0 and x_val < mXCord and y_val > 0 and y_val < mYCord):
                    if np.array_equal(pixels[x_val][y_val], (0,0,0)):
                        pixels[x_val][y_val] = colour

def rotate(coordinates, center, degrees):
    x = coordinates[0] - center[0]
    y = coordinates[1] - center[1]
    radians = math.radians(degrees)
    n_x = (x * math.cos(radians)) - (y * math.sin(radians))
    n_y = (y * math.cos(radians)) + (x * math.sin(radians))
    return [n_x + center[0], n_y + center[1]]

def decide_next(region_area, colour):
    #for now gonna do ugly code
    max_area = dp.region_max_area[colour]
    if region_area >= max_area:
        n_colour = dp.region_to[colour]
        transitions = dp.random_probs[n_colour]
        colours, probs = zip(*transitions)
        n_colour = random.choices(colours, weights=probs,k=1)[0]
        return 0, n_colour

    return region_area, colour

def draw_square(center, s_length, region_area, degrees_rotate, shrink_by, thickness, colour, pixels, iteration, max_depth, parent_side=None):
    region_area += s_length * s_length
    half_step = s_length / 2
    top_right = [center[0] + half_step, center[1] - half_step]
    top_left = [center[0] + half_step, center[1] + half_step]
    bott_right = [center[0] - half_step, center[1] - half_step]
    bott_left = [center[0] - half_step, center[1] + half_step]
    if (degrees_rotate != 0):
        top_right = rotate(top_right, center, degrees_rotate)
        top_left = rotate(top_left, center, degrees_rotate)
        bott_right = rotate(bott_right, center, degrees_rotate)
        bott_left = rotate(bott_left, center, degrees_rotate)
        fill_in_square(top_left, top_right, bott_left, bott_right, colour, pixels)
    lines = [[top_left, top_right], [top_right, bott_right], [bott_right, bott_left], [bott_left, top_left]]
    region_area, n_colour = decide_next(region_area, colour)
    for line_n, line in enumerate(lines):
        plot_line(line[0], line[1], thickness, colour, pixels)
        if line_n == parent_side:
            continue
        if iteration < max_depth:
            n_s_len = s_length * shrink_by
            n_half_step = n_s_len / 2
            n_center = []
            line_midpoint = [(line[0][0] + line[1][0]) / 2, (line[0][1] + line[1][1]) / 2]

            dx = line_midpoint[0] - center[0]
            dy = line_midpoint[1] - center[1]
            length = math.sqrt(dy**2 + dx**2)
            dy /= length
            dx /= length
            n_center = [
                    line_midpoint[0] + dx * n_half_step,                    line_midpoint[1] + dy * n_half_step
            ]

            next_parent_side = (line_n + 2) % 4
            draw_square(n_center, n_s_len, region_area, degrees_rotate, shrink_by, thickness, n_colour, pixels, iteration+1, max_depth, next_parent_side)

    


pixels = np.zeros((1000, 1000, 3), dtype=np.uint8)
draw_square([500,500], 100, 0, 10, 0.90, 1, (255, 255, 0), pixels, 0, 8)
img = Image.fromarray(pixels)
img.show()
