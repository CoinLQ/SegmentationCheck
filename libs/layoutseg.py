# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import io
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb
import sys, json
from operator import itemgetter

class BBoxLineRegion:
    def __init__(self):
        self.bbox_lst = []
        self.left = 10000
        self.right = 0

LEFT_MARKS = [u'<', u'【', u'@', u'(', u'$', u'{']
RIGHT_MARKS = [u'>', u'】', u'@', u')', u'$', u'}']

def binarisation_(src_image):
    if len(src_image.shape) == 3:
        image = (src_image.sum(axis=2) / 3).astype('ubyte')
    else:
        image = src_image
    block_size = 35
    binary = threshold_adaptive(image, block_size, offset=20)
    binary = binary.astype('ubyte')
    #im = (binary * 255).astype('ubyte')
    return binary


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
    #im = (binary * 255).astype('ubyte')
    #im = color.gray2rgb(binary)
    #im = (binary * 255).astype('ubyte')
    #im = cv2.GaussianBlur(im, (3, 3), 0)
    return binary

def add_to_region_lst(text, left, right, top, bottom, line_no, region_no, page_bar_no, region_lst, mark=None):
    region = {
        u'text': text,
        u'left': left,
        u'right': right,
        u'top': top,
        u'bottom': bottom,
        u'line_no': line_no,
        u'region_no': region_no,
        u'page_bar_no': page_bar_no,
    }
    if mark:
        region[u'mark'] = mark
    region_lst.append(region)

def find_min_pos(binary_line, start, middle, end):
    # 相对于start的坐标
    min_pos_up = np.argmin(binary_line[start : middle])
    min_pos_down = np.argmin(binary_line[middle: end]) + (middle - start)
    if binary_line[min_pos_up + start] < binary_line[min_pos_down + start]:
        min_pos = min_pos_up
    elif binary_line[min_pos_up + start] > binary_line[min_pos_down + start]:
        min_pos = min_pos_down
    else:
        if (middle - start - min_pos_up) < (min_pos_down - (middle - start)):
            min_pos = min_pos_up
        else:
            min_pos = min_pos_down
    return min_pos

def region_seg(image, binary_image, image_height, page_bar_no, line_no, line_region, text, region_lst):
    mark = None
    if text[0] == u'$' and text[-1] == u'$': # 一般$在首尾
        text = text[1: -1]
    elif text[0] == u'(' and text[-1] == u')':
        text = text[1: -1]
    elif text[0] == u'@' and text[-1] == u'@': # 一般@在首尾
        text = text[1: -1]
        mark = u'@'
    if u'(' in text or u')' in text:
        text = text.replace(u'(', u'').replace(u')', u'')
    if u'<' not in text and u'【' not in text:
        region = {
            u'text': text,
            u'left': line_region.left,
            u'right': line_region.right,
            u'top': 0,
            u'bottom': image_height,
            u'line_no': line_no,
            u'region_no': 1,
            u'page_bar_no': page_bar_no,
        }
        if mark:
            region[u'mark'] = mark
        region_lst.append(region)
        return

    # avg_height = 55
    # avg_small_height = 35

    # 洪武南藏
    avg_height = 51
    avg_small_height = 51

    binary = binary_image[:, line_region.left:line_region.right]
    binary_line = binary.sum(axis=1)

    region_width = line_region.right - line_region.left
    step = avg_height / 4 # region_width / 4
    start = 0
    end = image_height - 1
    for i in xrange(0, image_height, step):
        if np.sum(binary_line[i:i + step]) >= 10:
            start = i
            break
    for i in xrange(image_height - 1, 0, -step):
        if np.sum(binary_line[i:i + step]) >= 10:
            end = i
            break
    start = max(0, start - step)
    end = min(end + 1 + step, image_height)
    h = end - start

    if u'<' in text:
        right_small_cnt = 0
        left_small_cnt = 0
        right_small_flag = False
        left_small_flag = False
        char_cnt = len(text)
        equivalent_char_cnt = 0

        '''
        for ch_idx in range(char_cnt):
            ch = text[ch_idx]
            if ch == u'<':
                if ch_idx == 0:
                    right_small_flag = True
                elif text[ch_idx - 1] != u'>':
                    right_small_flag = True
                else:
                    left_small_flag = True
                    right_small_flag = False
            elif ch == u'>':
                if ch_idx == char_cnt - 1 or text[ch_idx+1] != u'<':
                    equivalent_char_cnt = equivalent_char_cnt + max(left_small_cnt, right_small_cnt)
                    left_small_cnt = 0
                    right_small_cnt = 0
                    left_small_flag = False
                    right_small_flag = False
            else:
                if not left_small_flag and not right_small_flag:
                    equivalent_char_cnt = equivalent_char_cnt + 1
                elif right_small_flag:
                    right_small_cnt = right_small_cnt + 1
                else:
                    left_small_cnt = left_small_cnt + 1
        avg_height = h * 1.0 / equivalent_char_cnt
        print 'avg_height: ', avg_height
        '''

        cur_pos = 0
        cur_start = start
        passed_char_cnt = 0
        passed_small_char_cnt = 0
        region_no = 1
        while cur_pos <= char_cnt - 3:
            right_mark_pos = text.find(u'<', cur_pos)
            if right_mark_pos == -1:
                break
            if cur_pos < right_mark_pos:
                passed_char_cnt = passed_char_cnt + (right_mark_pos - cur_pos)
                #y = int(passed_char_cnt * avg_height + passed_small_char_cnt * avg_small_height) + start
                y = cur_start - 1 + int((right_mark_pos - cur_pos) * avg_height)
                #print cur_pos, cur_start, y, text[cur_pos : right_mark_pos]
                if binary_line[y] != 0:
                    min_pos = np.argmin(binary_line[y - avg_height / 2: y + avg_height / 2])
                    y = min_pos + y - avg_height / 2
                #print cur_start, y+1, text[cur_pos : right_mark_pos]
                add_to_region_lst(text[cur_pos : right_mark_pos],
                                  line_region.left, line_region.right,
                                  cur_start, y+1,
                                  line_no, region_no,
                                  page_bar_no, region_lst)
                region_no = region_no + 1
                cur_start = y+1
            # right small
            right_end_mark_pos = text.find(u'>', right_mark_pos)
            if right_end_mark_pos != -1:
                if right_end_mark_pos != char_cnt - 1 and text[right_end_mark_pos + 1] == u'<':
                    # left , right 都存在
                    left_mark_pos = right_end_mark_pos + 1
                    left_end_mark_pos = text.find(u'>', left_mark_pos)
                    if left_end_mark_pos == char_cnt - 1:
                        y = end - 1
                    else:
                        right_small_cnt = right_end_mark_pos - right_mark_pos - 1
                        left_small_cnt = left_end_mark_pos - left_mark_pos - 1
                        passed_small_char_cnt = passed_small_char_cnt + max(right_small_cnt, left_small_cnt)
                        #y = int(passed_char_cnt * avg_height + passed_small_char_cnt * avg_small_height) + start
                        y = cur_start - 1 + int(max(right_small_cnt, left_small_cnt) * avg_small_height)
                        if binary_line[y] != 0:
                            #min_pos = np.argmin(binary_line[y - avg_small_height / 2: y + avg_small_height / 2])
                            min_pos = find_min_pos(binary_line, y - avg_small_height / 2, y, y + avg_small_height / 2)
                            y = min_pos + y - avg_small_height / 2

                    # right region
                    #print cur_start, y+1, (line_region.left + region_width / 2), line_region.right, \
                    #    text[right_mark_pos + 1: right_end_mark_pos]
                    add_to_region_lst(text[right_mark_pos + 1: right_end_mark_pos],
                                      line_region.left + region_width / 2, line_region.right,
                                      cur_start, y+1,
                                      line_no, region_no,
                                      page_bar_no, region_lst, u'<')
                    region_no = region_no + 1

                    # left region
                    #print cur_start, y+1, line_region.left, (line_region.right - region_width / 2), \
                    #    text[left_mark_pos + 1: left_end_mark_pos]
                    add_to_region_lst(text[left_mark_pos + 1: left_end_mark_pos],
                                      line_region.left, line_region.right - region_width / 2,
                                      cur_start, y+1,
                                      line_no, region_no,
                                      page_bar_no, region_lst, u'<')
                    region_no = region_no + 1

                    cur_pos = left_end_mark_pos + 1
                else:
                    # 只存在right
                    if right_end_mark_pos == char_cnt - 1:
                        y = end - 1
                    else:
                        right_small_cnt = right_end_mark_pos - right_mark_pos - 1
                        passed_small_char_cnt = passed_small_char_cnt + (right_end_mark_pos - right_mark_pos - 1)
                        #y = int(passed_char_cnt * avg_height + passed_small_char_cnt * avg_small_height) + start
                        y = cur_start - 1 + int(right_small_cnt * avg_small_height)
                        if binary_line[y] != 0:
                            #min_pos = np.argmin(binary_line[y - avg_small_height / 2: y + avg_small_height / 2])
                            min_pos = find_min_pos(binary_line, y - avg_small_height / 2, y, y + avg_small_height / 2)
                            y = min_pos + y - avg_small_height / 2
                    #print cur_start, y+1, (line_region.left + region_width/2), line_region.right, text[right_mark_pos + 1: right_end_mark_pos]
                    add_to_region_lst(text[right_mark_pos + 1: right_end_mark_pos],
                                          line_region.left + region_width / 2, line_region.right,
                                          cur_start, y+1,
                                          line_no, region_no,
                                          page_bar_no, region_lst, u'<')
                    region_no = region_no + 1

                    cur_pos = right_end_mark_pos + 1
                cur_start = y+1
        if cur_pos <= char_cnt - 1:
            #print cur_start, end, line_region.left, line_region.right, text[cur_pos:]
            add_to_region_lst(text[cur_pos: ],
                              line_region.left, line_region.right,
                              cur_start, end,
                              line_no, region_no,
                              page_bar_no, region_lst)

# 處理經過二值化的圖片
def layout_seg(img_path, page_text):
    image = io.imread(img_path, 0)
    texts = page_text.rstrip(u'\r\n').split(u'\r\n')
    bw = binarisation(image)
    image_height, image_width = bw.shape
    bw = (1 - bw).astype('ubyte')

    total_bbox_lst = []
    label_image = label(bw, connectivity=2)
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        total_bbox_lst.append( (minr, minc, maxr, maxc) )

    total_bbox_lst.sort(key=itemgetter(2), reverse=True)
    total_bbox_lst.sort(key=itemgetter(3), reverse=True)
    line_lst = []
    line_region = BBoxLineRegion()
    for bbox in total_bbox_lst:
        middle = (bbox[1] + bbox[3]) / 2
        if not line_region.bbox_lst:
            line_region.bbox_lst.append(bbox)
            line_region.left = bbox[1]
            line_region.right = bbox[3]
            continue
        line_middle = (line_region.left + line_region.right) / 2
        if (middle >= line_region.left and middle <= line_region.right) or (line_middle >= bbox[1] and line_middle <= bbox[3]):
            line_region.bbox_lst.append(bbox)
            if line_region.left > bbox[1]:
                line_region.left = bbox[1]
            if line_region.right < bbox[3]:
                line_region.right = bbox[3]
        else:
            if (line_region.right - line_region.left > 5):
                line_lst.append(line_region)
            line_region = BBoxLineRegion()
    if line_region.bbox_lst: # and (line_region.right - line_region.left > 5):
        line_lst.append(line_region)
    new_line_lst = []
    for line_region in line_lst:
        if line_region.right - line_region.left >= 25:
            new_line_lst.append(line_region)
        line_lst = new_line_lst
    for i in range(len(line_lst) - 1):
        distance = line_lst[i].left - line_lst[i+1].right
        if distance <= 25:
            middle = (line_lst[i].left + line_lst[i+1].right) / 2
            line_lst[i].left = middle
            line_lst[i + 1].right = middle

    region_lst = []
    line_idx = 0
    text_len = len(texts)
    page_bar_no = texts[0].strip()
    for i in range(1, text_len):
        text = texts[i].rstrip()
        if text:
            #left = line_lst[line_idx].left
            #right = line_lst[line_idx].right
            # region = {
            #     u'text': text,
            #     u'left': left,
            #     u'right': right,
            #     u'top': 0,
            #     u'bottom': image_height,
            #     u'line_no': i,
            #     u'region_no': 1,
            #     u'page_bar_no': page_bar_no,
            # }

            region_seg(image, bw, image_height, page_bar_no, i, line_lst[line_idx], text, region_lst)
            line_idx = line_idx + 1
            # if text[0] == u'$' and text[-1] == u'$':
            #     text = text[1 : -1]
            #     region[u'text'] = text
            # elif text[0] == u'(' and text[-1] == u')':
            #     text = text[1: -1]
            #     region[u'text'] = text
            # elif text[0] == u'@' and text[-1] == u'@':
            #     text = text[1 : -1]
            #     region[u'mark'] = u'@'
            #     region[u'text'] = text
            # if u'(' in text:
            #     text = text.replace(u'(', u'').replace(u')', u'')
            # if u'<' not in text and u'【' not in text:
            #     region_lst.append(region)
            #     line_idx = line_idx + 1
            # elif u'<' in text:
            #     right_small_cnt = 0
            #     left_small_cnt = 0
            #     right_small_flag = False
            #     left_small_flag = False
            #     char_cnt = len(text)
            #     equivalent_char_cnt = 0
            #
            #     for ch_idx in range(char_cnt):
            #         ch = text[ch_idx]
            #         if ch == u'<':
            #             if ch_idx == 0:
            #                 right_small_flag = True
            #             elif text[ch_idx-1] != u'>':
            #                 right_small_flag = True
            #             else:
            #                 left_small_flag = True
            #                 right_small_flag = False
            #         elif ch == u'>':
            #             if left_small_flag:
            #                 equivalent_char_cnt = equivalent_char_cnt + max(left_small_cnt, right_small_cnt)
            #         else:
            #             if not left_small_flag and not right_small_flag:
            #                 equivalent_char_cnt = equivalent_char_cnt + 1
            #             elif right_small_flag:
            #                 right_small_cnt = right_small_cnt + 1
            #             else:
            #                 left_small_cnt = left_small_cnt + 1


        else:
            left = line_lst[line_idx].right
            right = line_lst[line_idx-1].left
            region = {
                u'text': text,
                u'left': left,
                u'right': right,
                u'top': 0,
                u'bottom': image_height,
                u'line_no': i,
                u'region_no': 1,
                u'page_bar_no': page_bar_no,
            }
            region_lst.append(region)
    return region_lst

    '''
    label_image = label(bw, connectivity=2)
    image_label_overlay = label2rgb(label_image, image=image)

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    for region in regionprops(label_image):
        #if region.area < 10:
        #    continue
        #print region.coords

        # draw rectangle around segmented coins
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    ax.imshow(image_label_overlay)
    plt.show()
    #io.imsave(dst_image, image)
    '''

if __name__ == '__main__':
    img_path = sys.argv[1]
    text = u''
    with open(sys.argv[2], 'r') as f:
        text = f.read().decode('utf-8')
    region_lst = layout_seg(img_path, text)
    output = json.dumps(region_lst, ensure_ascii=False, indent=True)
    print output.encode('utf-8')
