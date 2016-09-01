# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import io
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb

import sys, json
from operator import itemgetter


class WhiteRegion:
    """
    [top, bottom]
    """
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.height = self.bottom - self.top + 1

    def set_top_bottom(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.height = self.bottom - self.top + 1

    def set_top(self, top):
        self.top = top
        self.height = self.bottom - self.top + 1

    def set_bottom(self, bottom):
        self.bottom = bottom
        self.height = self.bottom - self.top + 1

def find_top(binary_line, region_height, region_width, start):
    white_regions = []
    cur_white_region_top = -1
    cur_non_white_region_top = -1
    if binary_line[0] == 0:
        cur_white_region_top = 0
    else:
        cur_non_white_region_top = 0
    for i in range(start + 1, region_height):
        if binary_line[i] == 0:
            if binary_line[i - 1] != 0:  # i is the begin of a new white region
                cur_white_region_top = i
                if i - cur_non_white_region_top >= region_width:
                    break
        else:
            if binary_line[i - 1] == 0:  # i is the begin of a new non-white region
                cur_non_white_region_top = i
                white_regions.append(WhiteRegion(cur_white_region_top, i - 1))
    while (white_regions and white_regions[-1].height < region_width / 2):
        white_regions.pop()
    # 合并相邻的空白区域
    pop_index = []
    white_regions_length = len(white_regions)
    for i in range(white_regions_length - 1):
        if (white_regions[i + 1].top - white_regions[i].bottom) <= 10:
            white_regions[i + 1].set_top(white_regions[i].top)
            pop_index.append(i)
    if pop_index:
        new_white_regions = []
        for i in range(white_regions_length):
            if i not in pop_index:
                new_white_regions.append(white_regions[i])
        white_regions = new_white_regions
    if white_regions:
        top = white_regions[0].bottom
    else:
        top = 0
    return top

def charseg(image, binary_image, region_lst, page_id):
    char_lst = []
    for region in region_lst:
        region_top = region[u'top']
        region_bottom = region[u'bottom']
        region_left = region[u'left']
        region_right = region[u'right']
        text = region[u'text']
        line_no = region[u'line_no']
        region_no = region[u'region_no']
        region_image = image[region_top : region_bottom, region_left : region_right]
        binary_region_image = binary_image[region_top: region_bottom, region_left: region_right]
        binary = (binary_region_image / 255).astype('ubyte')
        binary = 1 - binary
        binary_line = binary.sum(axis=1)
        height = region_bottom - region_top
        region_width = region_right - region_left
        step = 5
        start = 0
        end = height - 1
        for i in xrange(0, height, step):
            if np.sum(binary_line[i:i+step]) >= 10:
                start = i
                break
        for i in xrange(height - 1, 0, -step):
            if np.sum(binary_line[i:i+step]) >= 10:
                end = i
                break
        start = max(0, start - step)
        end = min(end + 1 + step, height)
        h = end - start
        text = text.strip(u'　')
        if u'　' not in text:
            char_count = len(text)
            if not char_count:
                continue
            avg_height = h * 1.0 / char_count
            rel_top = 0
            rel_bottom = 0
            for i in range(char_count):
                if rel_bottom:
                    rel_top = rel_bottom
                else:
                    rel_top = int(i * avg_height) + start
                #rel_top = int(i * avg_height) + start
                rel_bottom = rel_top + int(avg_height)
                #rel_bottom = int((i + 1) * avg_height) + start
                if rel_bottom >= end:
                    rel_bottom = end
                if binary_line[rel_bottom - 1] != 0:
                    min_pos = np.argmin(binary_line[rel_bottom - int(avg_height/3): rel_bottom + int(avg_height/3)])
                    rel_bottom = min_pos + rel_bottom - int(avg_height/3) + 1
                top = rel_top + region_top
                bottom = rel_bottom + region_top
                char_no = i + 1
                char = {
                    u'top': top,
                    u'bottom': bottom,
                    u'left': region_left,
                    u'right': region_right,
                    u'char': text[i],
                    u'line_no': line_no,
                    u'region_no': region_no,
                    u'char_no': char_no,
                }
                char_lst.append(char)
                char_image = region_image[rel_top: rel_bottom]
                char_filename = u'%s-%s-%s-%s.jpg' % (page_id, line_no, region_no, char_no)
                io.imsave(char_filename, char_image)
        else:
            text_segs = text.split(u'　')
            text_segs_cnt = len(text_segs)
            cur_pos = start
            start_pos = start
            added_char_count = 0

            for text_segs_idx in range(text_segs_cnt):
                start_pos = cur_pos
                txt = text_segs[text_segs_idx]
                if text_segs_idx != text_segs_cnt - 1:
                    white_region_start = -1
                    white_region_end = -1
                    for j in xrange(cur_pos, height, step):
                        if white_region_start == -1:
                            if np.sum(binary_line[j:j+region_width]) == 0:
                                white_region_start = j + step
                        else:
                            if np.sum(binary_line[j:j+step]) >= 10:
                                white_region_end = j - step
                                if white_region_end - white_region_start >= region_width:
                                    break
                    end_pos = white_region_start
                    h = end_pos - cur_pos
                    cur_pos = white_region_end
                else:
                    end_pos = end
                    h = end_pos - cur_pos
                    cur_pos = end
                print txt
                char_count = len(txt)
                if not char_count:
                    continue
                avg_height = h * 1.0 / char_count
                rel_top = 0
                rel_bottom = 0
                for i in range(char_count):
                    if rel_bottom:
                        rel_top = rel_bottom
                    else:
                        rel_top = int(i * avg_height) + start_pos
                    #rel_top = int(i * avg_height) + start_pos
                    rel_bottom = rel_top + int(avg_height) #int((i + 1) * avg_height) + start_pos
                    if rel_bottom >= end_pos:
                        rel_bottom = end_pos
                    print rel_bottom
                    if binary_line[rel_bottom - 1] != 0:
                        min_pos = np.argmin(binary_line[rel_bottom - int(avg_height/3) : rel_bottom + int(avg_height/3)])
                        rel_bottom = min_pos + rel_bottom - int(avg_height/3) + 1

                    top = rel_top + region_top
                    bottom = rel_bottom + region_top
                    added_char_count = added_char_count + 1
                    char_no = added_char_count
                    char = {
                        u'top': top,
                        u'bottom': bottom,
                        u'left': region_left,
                        u'right': region_right,
                        u'char': txt[i],
                        u'line_no': line_no,
                        u'region_no': region_no,
                        u'char_no': char_no,
                    }
                    char_lst.append(char)
                    if rel_top >= rel_bottom:
                        print txt[i], char
                    print rel_top, rel_bottom
                    char_image = region_image[rel_top: rel_bottom]
                    char_filename = u'%s-%s-%s-%s.jpg' % (page_id, line_no, region_no, char_no)
                    io.imsave(char_filename, char_image)
    return char_lst

def binarisation(src_image):
    if len(src_image.shape) == 3:
        image = (src_image.sum(axis=2) / 3).astype('ubyte')
    else:
        image = src_image
    thresh = threshold_otsu(image)
    binary = (image > thresh).astype('ubyte')
    binary1 = 1 - binary
    im = 255 - np.multiply(255 - image, binary1)
    block_size = 35
    binary = threshold_adaptive(image, block_size, offset=20)
    binary = binary.astype('ubyte')
    return binary

if __name__ == '__main__':
    src_image = io.imread(sys.argv[1], 0)
    if len(sys.argv) == 4 and sys.argv[3] == 'binary':
        binary = binarisation(src_image)
        binary_image = (binary * 255).astype('ubyte')
    else:
        binary_image = src_image
    page_id = sys.argv[1][:-4]
    with open(sys.argv[2], 'r') as f:
        region_lst = json.load(f, 'utf-8')
        char_lst = charseg(src_image, binary_image, region_lst, page_id.decode('utf-8'))
        output = json.dumps(char_lst, ensure_ascii=False, indent=True)
        print output.encode('utf-8')