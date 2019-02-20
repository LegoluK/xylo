#!/usr/bin/env python3

from PIL import Image
from enum import Enum
import numpy as np
import sys

def draw_square_around(array, color, center, length):
    ww = max(0, center[0] - length//2), min(array.shape[1] - 1, center[0] + length//2)
    hh = max(0, center[1] - length//2), min(array.shape[0], center[1] + length//2)
    for h in hh:
        for w in range(*ww):
            array[h][w] = color
    for w in ww:
        for h in range(*hh):
            array[h][w] = color

if (len(sys.argv) < 3):
    print("Input and output images expected")
    sys.exit(1)
image_in = Image.open(sys.argv[1])
width, height = image_in.size
image_array = np.array(image_in)

class State(Enum):
    START = 0
    STOP = 1
    NOTHING = 2

last_line = [(State.NOTHING, 0, 0) for i in range(width)] # state area perimeter
threshold = 0.9 * (3 * 255)
area_min = 10
area_max = 200
circularity_min = 0.3

indices_max = []
show_thresholded_image = False
for h in range(height):
    bright_beginning = 0
    bright_pixel_last = 0
    bright_up = False
    area_up = 0
    area = 0
    perimeter = 0
    perimeter_up = 0
    overlap_start = 0
    overlap = False
    has_child = False
    for w in range(width):
        y = sum(image_array[h][w])
        bright_pixel = 1 if y >= threshold else 0
        new_pixel = 255 * bright_pixel
        if show_thresholded_image:
            image_array[h][w] = [new_pixel, new_pixel, new_pixel]
        start = bright_pixel == 1 and bright_pixel_last == 0 # bright_pixel > bright_pixel_last
        stop = bright_pixel == 0 and bright_pixel_last == 1 # bright_pixel < bright_pixel_last
        bright_pixel_last = bright_pixel
        start_up, a, p = last_line[w]
        last_line[w] = 0, 0, 0
        if start_up == State.START:
            bright_up = True
        elif start_up == State.STOP:
            bright_up = False
        if start_up == State.START:
            has_child = False
            area_up = a
            perimeter_up = p
        if ((start_up == State.START) and bright_pixel) or (start and bright_up):
            overlap_start = w
            overlap = True
        if ((start_up == State.STOP) or stop) and overlap:
            perimeter -= 2 * (w - overlap_start)
            overlap = False
        has_child |= bright_pixel
        if start_up == State.STOP:
            area += area_up
            perimeter += perimeter_up
            if not has_child:
                circularity = (4 * np.pi * area_up) / (perimeter_up * perimeter_up)
                if area_up > area_min and area_up < area_max and circularity > circularity_min:
                    print("found a blob: ", area_up, perimeter_up, "circularity:", circularity)
                    indices_max.append((w, h)) # TODO: point at the center
        if start:
            bright_beginning = w
            area = 0
            perimeter = 2
        if stop:
            area += (w - 1) - bright_beginning + 1
            perimeter += 2 * (w - bright_beginning)
            if bright_up:
                area += area_up
                perimeter += perimeter_up
            last_line[bright_beginning] = State.START, area, perimeter
            last_line[w] = State.STOP, 0, 0

for index_max in indices_max:
    draw_square_around(image_array, (0, 255, 0), index_max, height//12)

image_out = Image.fromarray(image_array)
image_out.save(sys.argv[2])
