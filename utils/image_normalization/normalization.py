# coding: utf-8

import skimage.io as io
import skimage.filters as filters
import numpy as np
import sys
import os

def nln(src_image):
    orig_image = io.imread(src_image, 0)
    if len(orig_image.shape) == 3:
        image = (orig_image.sum(axis=2) / 3).astype('ubyte')
    else:
        image = orig_image
    h, w = image.shape
    thresh = filters.threshold_otsu(image)
    binary = (image < thresh).astype('ubyte') # 二值化，黑色为1
    sum_of_black_pixels = np.sum(binary)
    if sum_of_black_pixels == 0:
        raise Exception("white or black image.")
    binary_line = binary.sum(axis=0) # 在X轴上投影
    hx = binary_line / (sum_of_black_pixels * 1.0)
    binary_line_v = binary.sum(axis=1) # 在Y轴上投影
    hy = binary_line_v / (sum_of_black_pixels * 1.0)

    H = 32
    W = 32
    binary_new = np.zeros( (H, W) )
    for y in range(h):
        for x in range(w):
            if binary[y,x] == 1:
                x2 = int((W-1) * np.sum(hx[0:x+1]))
                y2 = int((H-1) * np.sum(hy[0:y+1]))
                x2_end = int((W - 1) * np.sum(hx[0:x + 2]))
                y2_end = int((H - 1) * np.sum(hy[0:y + 2]))
                if y == h - 1:
                    y2 = H - 1
                    y2_end = H
                if x == w - 1:
                    x2 = W - 1
                    x2_end = W
                binary_new[y2:y2_end, x2:x2_end] = binary[y,x]
    return binary_new.astype('ubyte')

def normalize(char):
    image_path = char.get_image_path()
    nln_path = char.npy_path()
    if os.path.exists(nln_path):
        binary = np.load(nln_path)
    else:
        binary = nln(image_path)
        np.save(nln_path, binary)
    return binary

if __name__ == '__main__':
    image_norm = nln(sys.argv[1])
    image = np.tile(image_norm[:, :, np.newaxis], [1, 1, 3]) * 255
    image = image.astype('ubyte')
    io.imsave('./out/' + sys.argv[1].replace('.jpg', '.bmp'), image)