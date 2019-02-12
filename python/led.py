#!/usr/bin/env python3

from PIL import Image
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

index_max = 0, 0
max_element = 0
for h in range(height):
    for w in range(width):
        if (sum(image_array[h][w]) > max_element):
            index_max = w, h
            max_element = sum(image_array[h][w])
print(index_max)
print(max_element/(3*255))
draw_square_around(image_array, (0, 255, 0), index_max, height//8)

image_out = Image.fromarray(image_array)
image_out.save(sys.argv[2])
