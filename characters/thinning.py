# coding: utf-8
from scipy import weave
import numpy as np
import sys
from skimage import io
from skimage.filters import threshold_otsu
from skimage.transform import resize

def binarisation(src_image):
    if len(src_image.shape) == 3:
        image = (src_image.sum(axis=2) / 3).astype('ubyte')
    else:
        image = src_image
    thresh = threshold_otsu(image)
    binary = (image > thresh).astype('ubyte')
    return binary

def _thinningIteration(im, iter):
    I, M = im, np.zeros(im.shape, np.uint8)
    expr = """
    for (int i = 1; i < NI[0]-1; i++) {
        for (int j = 1; j < NI[1]-1; j++) {
            int p2 = I2(i-1, j);
            int p3 = I2(i-1, j+1);
            int p4 = I2(i, j+1);
            int p5 = I2(i+1, j+1);
            int p6 = I2(i+1, j);
            int p7 = I2(i+1, j-1);
            int p8 = I2(i, j-1);
            int p9 = I2(i-1, j-1);
            int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) +
                     (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) +
                     (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
                     (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
            int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            int m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            int m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);
            if (A == 1 && B >= 2 && B <= 6 && m1 == 0 && m2 == 0) {
                M2(i,j) = 1;
            }
        }
    }
    """

    weave.inline(expr, ["I", "iter", "M"])
    return (I & ~M)


def thinning(src):
    dst = src.copy() # / 255
    prev = np.zeros(src.shape[:2], np.uint8)
    diff = None

    while True:
        dst = _thinningIteration(dst, 0)
        dst = _thinningIteration(dst, 1)
        diff = np.absolute(dst - prev)
        prev = dst.copy()
        if np.sum(diff) == 0:
            break

    return dst # * 255

def convert_image(src_image):
    image = io.imread(src_image, 0)
    try:
        bw = binarisation(image)
    except:
        return None
    bw = 1 - bw
    image_height, image_width = bw.shape
    binary_line = bw.sum(axis=0)
    c_start = -1
    c_end = -1
    r_start = -1
    r_end = -1
    for i in range(image_width):
        if binary_line[i] != 0:
            c_start = i
            break
    for i in range(image_width-1, 0, -1):
        if binary_line[i] != 0:
            c_end = i + 1
            break

    binary_line = bw.sum(axis=1)
    for i in range(image_width):
        if binary_line[i] != 0:
            r_start = i
            break
    for i in range(image_height-1, 0, -1):
        if binary_line[i] != 0:
            r_end = i + 1
            break
    #print r_start, r_end, c_start, c_end
    if c_start == -1 or c_end == -1 or r_start == -1 or r_end == -1:
        return None
    image_new = bw[r_start:r_end, c_start:c_end]
    # 高度缩放到20，宽度等比例
    H = 20
    W = 32
    new_width = int(H * 1.0 / image_height * image_width)
    new_width = min(W, new_width)
    image_resize = 255 * resize(image_new, (H, new_width), mode='edge', preserve_range=True)
    image_resize = image_resize.astype('ubyte')
    image_resize = binarisation(image_resize)
    # 宽度填充到W
    if W > new_width:
        left_pad = (W - new_width) / 2
        right_pad = W - new_width - left_pad
        image_norm = np.zeros( (H, W) )
        image_norm[:, left_pad : W-right_pad] = image_resize
        return image_norm.astype('ubyte')
    else:
        return image_resize

if __name__ == '__main__':
    image_norm = convert_image(sys.argv[1])
    image_norm = thinning(image_norm)
    image = np.tile(image_norm[:, :, np.newaxis], [1, 1, 3]) * 255
    image = image.astype('ubyte')
    io.imsave('./out/' + sys.argv[1].replace('.jpg', '.bmp'), image)