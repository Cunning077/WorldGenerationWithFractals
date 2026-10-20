import numpy as np
from PIL import Image
import math

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
                    pixels[y_val][x_val] = colour

def rotate(coordinates, center, degrees):
    x = coordinates[0] - center[0]
    y = coordinates[1] - center[1]
    radians = math.radians(degrees)
    n_x = (x * math.cos(radians)) - (y * math.sin(radians))
    n_y = (y * math.cos(radians)) + (x * math.sin(radians))
    return [n_x + center[0], n_y + center[1]]


def draw_triangle(center, s_length, degrees_rotate, thickness, colour, pixels, shrink_side_by, iteration, max_depth):
    triangle_height = round(s_length * math.sqrt(3)/2)
    top = [center[0] - triangle_height/2, center[1]]
    bottom_left = [center[0] + triangle_height/2, center[1] - s_length/2]
    bottom_right = [center[0] + triangle_height/2, center[1] + s_length/2]
    if (degrees_rotate != 0):
        top = rotate(top, center, degrees_rotate)
        bottom_left = rotate(bottom_left, center, degrees_rotate)
        bottom_right = rotate(bottom_right, center, degrees_rotate)
    lines = [[top, bottom_left],[top, bottom_right], [bottom_left, bottom_right]]
    line_number = 0
    for line in lines:
        line_number += 1
        plot_line(line[0], line[1], thickness, colour, pixels)
        if (iteration < max_depth and (iteration < 1 or line_number < 3)):
            dy = line[1][0] - line[0][0]
            dx = line[1][1] - line[0][1]
            gradient = dy / dx if dx != 0 else float('inf')
            new_side_length = s_length * shrink_side_by
            center_of_line = [(line[0][0] + line[1][0]) / 2, 
                              (line[0][1] + line[1][1]) / 2]
            new_center = []
            new_rotation = degrees_rotate
            if (line_number == 1):
                new_rotation += 60
            elif (line_number == 2):
                new_rotation -= 60
            else:
                new_rotation += 180
            if (gradient < 0.0001 and gradient > -0.0001):
                if (center_of_line[0] - center[0] > 0):
                    new_center = [center_of_line[0] + triangle_height * 
                                 (shrink_side_by/2), center_of_line[1]]
                else:
                    new_center = [center_of_line[0] - triangle_height * 
                                  (shrink_side_by/2), center_of_line[1]]

            else:
                center_of_line = [
                    (line[0][0] + line[1][0]) / 2,
                    (line[0][1] + line[1][1]) / 2
                ]
                dy = line[1][0] - line[0][0]
                dx = line[1][1] - line[0][1]
                perp_y = dx
                perp_x = -dy
                to_mid_y = center_of_line[0] - center[0]
                to_mid_x = center_of_line[1] - center[1]

                if perp_y * to_mid_y + perp_x * to_mid_x < 0:
                    perp_y *= -1
                    perp_x *= -1
                length = math.sqrt(perp_y**2 + perp_x**2)
                perp_y /= length
                perp_x /= length

                distance_from_center = triangle_height * shrink_side_by / 2

                new_center = [
                    center_of_line[0] + perp_y * distance_from_center,
                    center_of_line[1] + perp_x * distance_from_center
                ]
            draw_triangle(new_center, new_side_length, new_rotation, 
                          thickness, colour, pixels, shrink_side_by, 
                          iteration+1, max_depth)


pixels = np.zeros((1000, 1000, 3), dtype=np.uint8)

draw_triangle(
    center=[500, 500],  # Center of the triangle
    s_length=200,       # Side length
    degrees_rotate=0,   # Rotation in degrees
    thickness= 1,        # Line thickness
    colour=(255, 200, 0), # yellow
    pixels=pixels,      # Pixel grid
    shrink_side_by=0.75, # Each recursive triangle is half the size
    iteration=0,        # Starting recursion depth
    max_depth=3         # Maximum recursion depth
)
img = Image.fromarray(pixels)
img.show()

