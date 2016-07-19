# coding: utf-8
import matplotlib
import matplotlib.pyplot as plt
import skimage.io as io

try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters
import numpy as np
from operator import attrgetter
import traceback

matplotlib.rcParams['font.size'] = 9

LINE_WIDTH = 55

class Char:
    def __init__(self, char, left, right, top, bottom, line_no, char_no, char_id=None):
        self.char = char
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.height = self.bottom - self.top
        self.line_no = line_no
        self.char_no = char_no
        self.char_id = char_id

    def set_top_bottom(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.height = self.bottom - self.top

    def set_char_no(self, char_no):
        self.char_no = char_no

    def set_char_id(self, char_id):
        self.char_id = char_id

    def set_char(self, char):
        self.char = char

    def cut_char_image(self, line_image):
        char_image = 1 - line_image[self.top:self.bottom, :]
        image = np.tile(char_image[:, :, np.newaxis], [1, 1, 3]) * 255
        image = image.astype('ubyte')
        io.imsave(u'/home/share/dzj_characters/character_images/%s.jpg' % self.char_id.strip(), image)

class LineRegion:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.width = self.right - self.left

    def set_left(self, left):
        self.left = left
        self.width = self.right - self.left

    def set_right(self, right):
        self.right = right
        self.width = self.right - self.left

def process_page1(image, text, page_id):
    thresh = filters.threshold_otsu(image)
    binary = (image > thresh).astype('ubyte')
    if len(binary.shape) == 3:
        binary = binary.sum(axis=2) / 3
    binary = 1 - binary
    image_height, image_width = binary.shape

    binary_line = binary.sum(axis=0)

    x_ax = np.arange(1, image_width + 1)
    y_ax = np.arange(1, image_height + 1)

    min_v = binary_line.min()
    max_v = binary_line.max()
    cut_thresh = min_v + (max_v - min_v) / 25
    #print 'min, max, cut_thresh', min_v, max_v, cut_thresh

    bins = []
    data = []
    for i in range(image_width):
        if binary_line[i] <= cut_thresh:
            bins.append(i)
            data.append(binary_line[i])

    new_bins = []
    new_data = []
    last_x = 0
    white_region = []
    for i in range(len(bins)):
        if (bins[i] - last_x) <= 1:
            white_region.append(i)
            last_x = bins[i]
        else:
            #print 'bins[i]: ', bins[i], last_x, white_region
            if len(new_bins) == 0:
                if len(white_region) > 0:
                    x = last_x - (last_x - bins[white_region[-1]]) / 10
                else:
                    x = last_x
                new_bins.append(x)
                new_data.append(binary_line[x])
            else:
                x = (bins[white_region[0]] + bins[white_region[-1]]) / 2
                new_bins.append(x)
                new_data.append(binary_line[x])
            white_region = [i]
            last_x = bins[i]
    # last white region
    if len(white_region) > 0:
        x = bins[white_region[0]] + (bins[white_region[-1]] - bins[white_region[0]]) / 10
        new_bins.append(x)
        new_data.append(binary_line[x])
        #print 'last white region: ', x

    for i in range(len(new_bins) - 1):
        end_x = new_bins[i+1]
        insert_pos = i + 1
        start_x = new_bins[i]

        while True:
            width = end_x - start_x
            if width >= LINE_WIDTH * 2: # cut
                cut_x = np.argmin(
                    binary_line[start_x + LINE_WIDTH / 2: start_x + LINE_WIDTH * 3 / 2 + 1]) + start_x + LINE_WIDTH / 2
                #print 'add cut_x: ', cut_x
                new_bins.insert(insert_pos, cut_x)
                insert_pos = insert_pos + 1
                start_x = cut_x
            else:
                break

    #plt.imshow(image)
    #plt.plot(x_ax, binary_line, 'b')
    #plt.bar(new_bins, [image_height] * len(new_bins), facecolor='red', edgecolor='red')

    # char segmentation for each line
    line_texts = text.rstrip().split(u'\n')
    line_count = len(line_texts)
    total_char_lst = []

    line_no = 0
    last_x = new_bins[-1]
    for i in range(len(new_bins) - 2, -1, -1):
        line_width = last_x - new_bins[i]
        if line_width < 15:
            last_x = new_bins[i]
            continue
        line_char_lst = []
        line_image = binary[:, new_bins[i]:last_x + 1]
        binary_line_vertical = line_image.sum(axis=1)
        line_min_v = binary_line_vertical.min()
        line_max_v = binary_line_vertical.max()
        if line_max_v < line_width / 10.0:
            last_x = new_bins[i]
            continue

        line_no = line_no + 1
        if line_no > line_count:  # 不处理超出文字行数的行
            break
        line_id = page_id + u'%02dL' % line_no
        #print u'#### line %s: %s ####' % (line_no, line_id)
        line_text = line_texts[line_no - 1]
        if line_text.find(u'<') != -1:  # 这一行有<，表示有小字，不处理
            last_x = new_bins[i]
            continue
        space_pos = line_text.find(u';')
        if space_pos != -1:
            line_chars = line_text[space_pos + 1:].strip()
        else:
            line_chars = line_text.strip()
        line_chars = filter(lambda x: x != u' ', line_chars)
        #print line_chars
        char_idx = 0

        line_bins = []
        line_data = []
        for j in range(image_height):
            if binary_line_vertical[j] <= line_min_v: # + (line_max_v-line_min_v)/25:
                line_bins.append(j)
                line_data.append(binary_line_vertical[j])
        line_new_bins = []
        line_new_data = []
        last_y = 0
        white_region = []
        last_white_region_bottom = 0
        for j in range(len(line_bins) + 1):
            process_cut_lines = False
            # last white region
            if j == len(line_bins):
                if len(white_region) > 0:
                    y = line_bins[white_region[0]] + (line_bins[white_region[-1]] - line_bins[white_region[0]]) / 25
                    process_cut_lines = True
            elif (line_bins[j] - last_y) <= 1:
                # print 'add white_region line:', line_bins[j]
                white_region.append(j)
                last_y = line_bins[j]
            else:
                # print 'new white_region line:', line_bins[j]
                # process last white region
                if len(white_region) > 0:
                    if len(line_new_bins) == 0:  # the first white region
                        y = last_y  # - min((last_y - line_bins[white_region[0]]) / 25, 2)
                        if j < len(line_bins) - 1:
                            line_new_bins.append(y)
                            line_new_data.append(binary_line_vertical[y])
                    else:
                        char_height1 = line_bins[white_region[0]] - line_new_bins[-1]
                        char_height2 = line_bins[j] - line_bins[white_region[-1]]
                        offset = (line_bins[white_region[-1]] - line_bins[white_region[0]]) * char_height2 / (
                        char_height1 + char_height2)
                        y = line_bins[white_region[0]] + offset
                        # y = (line_bins[white_region[0]] + line_bins[white_region[-1]])/2
                        process_cut_lines = True
                white_region = [j]
                last_y = line_bins[j]

            if process_cut_lines and len(line_new_bins) > 0 and char_idx < len(line_chars):
                y0 = line_new_bins[-1]
                char_height = y - y0
                height_width_ratio = (char_height * 1.0) / line_width
                ignore_ratio = 0.45

                if line_chars[char_idx] in [u'三']:
                    ignore_ratio = 0.55
                if height_width_ratio < ignore_ratio:
                    # line_new_bins.append(y)
                    # line_new_data.append(binary_line_vertical[y])
                    pass
                elif height_width_ratio > 1.4 and height_width_ratio < 2.1 and char_idx < (len(line_chars) - 1):  # 2 chars
                    #print '2 chars'
                    # find cut line between [y0 + char_height / 4, y - char_height / 4]
                    cut_y = np.argmin(
                        binary_line_vertical[y0 + char_height / 4: y - char_height / 4 + 1]) + y0 + char_height / 4
                    #print 'add cut_y: ', cut_y
                    ch = Char(line_chars[char_idx], new_bins[i], last_x, line_new_bins[-1], cut_y, line_no,
                              char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                    line_char_lst.append(ch)
                    char_idx += 1
                    line_new_bins.append(cut_y)
                    line_new_data.append(binary_line_vertical[cut_y])

                    ch = Char(line_chars[char_idx], new_bins[i], last_x, line_new_bins[-1], y, line_no, char_idx + 1,
                              line_id + u'%02d' % (char_idx + 1))
                    line_char_lst.append(ch)
                    char_idx += 1
                    line_new_bins.append(y)
                    line_new_data.append(binary_line_vertical[y])
                elif height_width_ratio > 2.1 and height_width_ratio < 2.8 and char_idx < (len(line_chars) - 2):  # 3 chars
                    # find cut line
                    #print '3 chars'
                    cut_y = np.argmin(
                        binary_line_vertical[y0 + char_height / 6: y0 + char_height / 2]) + y0 + char_height / 6
                    #print 'add cut_y: ', cut_y
                    ch = Char(line_chars[char_idx], new_bins[i], last_x, line_new_bins[-1], cut_y, line_no,
                              char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                    line_char_lst.append(ch)
                    char_idx += 1
                    line_new_bins.append(cut_y)
                    line_new_data.append(binary_line_vertical[cut_y])
                    cut_y = np.argmin(binary_line_vertical[
                                      y0 + char_height * 3 / 6: y0 + char_height * 5 / 6]) + y0 + char_height * 3 / 6
                    #print y, y0, char_height
                    #print 'between: ', y0 + char_height * 3 / 6, y0 + char_height * 5 / 6
                    #print 'add cut_y: ', cut_y, (y0 + char_height * 3 / 6)
                    ch = Char(line_chars[char_idx], new_bins[i], last_x, line_new_bins[-1], cut_y, line_no,
                              char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                    line_char_lst.append(ch)
                    char_idx += 1
                    line_new_bins.append(cut_y)
                    line_new_data.append(binary_line_vertical[cut_y])
                    ch = Char(line_chars[char_idx], new_bins[i], last_x, line_new_bins[-1], y, line_no, char_idx + 1,
                              line_id + u'%02d' % (char_idx + 1))
                    line_char_lst.append(ch)
                    char_idx += 1
                    line_new_bins.append(y)
                    line_new_data.append(binary_line_vertical[y])
                else:
                    ch = Char(line_chars[char_idx], new_bins[i], last_x, line_new_bins[-1], y, line_no, char_idx + 1,
                              line_id + u'%02d' % (char_idx + 1))
                    line_char_lst.append(ch)
                    char_idx += 1
                    line_new_bins.append(y)
                    line_new_data.append(binary_line_vertical[y])

        remained_count = len(line_chars) - len(line_char_lst)
        for j in range(remained_count):
            # 找到切分图像高度最大的字
            line_char_lst.sort(key = lambda ch: (ch.bottom - ch.top))
            if len(line_char_lst) >= 1:
                last_char = line_char_lst[-1]
                line_char_lst.remove(last_char)
                # 对char_no > last_char.char_no的字调整字符、char_no
                for ch in line_char_lst:
                    if ch.char_no > last_char.char_no:
                        ch.char_no = ch.char_no + 1
                        ch.char = line_chars[ch.char_no - 1]
                char_height = last_char.bottom - last_char.top
                #print 'remained cut: ', char_height
                char_idx = last_char.char_no - 1
                char_line_vertical = binary_line_vertical[last_char.top + char_height / 4: last_char.bottom - char_height / 4]
                cut_y = np.argmin(char_line_vertical) + last_char.top + char_height / 4
                #print 'add cut_y: ', cut_y
                line_new_bins.append(cut_y)
                line_new_data.append(binary_line_vertical[cut_y])
                ch = Char(line_chars[char_idx], last_char.left, last_char.right, last_char.top, cut_y, last_char.line_no,
                          char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                ch = Char(line_chars[char_idx + 1], last_char.left, last_char.right, cut_y, last_char.bottom, last_char.line_no,
                          char_idx + 2, line_id + u'%02d' % (char_idx + 2))
                line_char_lst.append(ch)

        for ch in line_char_lst:
            try:
                ch.cut_char_image(line_image)
                total_char_lst.append(ch)
            except:
                traceback.print_exc()

        #plt.plot(binary_line_vertical+last_x, y_ax, 'b')
        #plt.barh(line_new_bins, [line_width] * len(line_new_bins), left=new_bins[i], facecolor='red', edgecolor='red')
        last_x = new_bins[i]

    return total_char_lst


def process_line(line_image, binary_line_vertical,
                 line_top, line_bottom, line_left, line_right,
                 line_chars, line_id, line_no, total_char_lst,
                 image_height):
    line_chars = filter(lambda x: x != u' ', line_chars)
    char_idx = 0

    line_bins = []
    line_data = []
    line_height = binary_line_vertical.shape[0]
    line_min_v = binary_line_vertical.min()
    line_width = line_right - line_left
    line_char_lst = []

    for j in range(line_height):
        if binary_line_vertical[j] <= line_min_v:  # + (line_max_v-line_min_v)/25:
            # if line_no == 19:
            #    print j, line_bins, line_width * 1.2
            if len(line_bins) != 0:
                height = j - line_bins[-1]
                if height > line_width * 1.2:
                    cut_y = np.argmin(
                        binary_line_vertical[line_bins[-1] + height / 4: j - height / 4]) + line_bins[-1] + height / 4
                    line_bins.append(cut_y)
                    line_data.append(binary_line_vertical[cut_y])

            line_bins.append(j)
            line_data.append(binary_line_vertical[j])
    line_new_bins = []
    line_new_data = []
    last_y = 0
    white_region = []
    last_white_region_bottom = 0

    line_region_max = line_height - 1
    for j in range(line_height - 1, 0, -1):
        if binary_line_vertical[j] > line_min_v:
            break
        line_region_max = j

    for j in range(len(line_bins) + 1):
        process_cut_lines = False

        # the last white region
        if j == len(line_bins):
            #print line_top + line_bins[white_region[0]], line_top + line_bins[white_region[-1]]
            if len(white_region) > 0:
                y = line_bins[white_region[0]] + (line_bins[white_region[-1]] - line_bins[white_region[0]]) / 25
                process_cut_lines = True
        elif (line_bins[j] - last_y) <= 1:
            # print 'add white_region line:', line_bins[j]
            white_region.append(j)
            last_y = line_bins[j]
        else:
            # print 'new white_region line:', line_bins[j]
            # process last white region
            if len(white_region) > 0:
                if len(line_new_bins) == 0:  # the first white region
                    y = max(last_y - 10, 0)  # - min((last_y - line_bins[white_region[0]]) / 25, 2)
                    if j < len(line_bins) - 1:
                        line_new_bins.append(y)
                        line_new_data.append(binary_line_vertical[y])
                else:
                    char_height1 = line_bins[white_region[0]] - line_new_bins[-1]
                    char_height2 = line_bins[j] - line_bins[white_region[-1]]
                    offset = (line_bins[white_region[-1]] - line_bins[white_region[0]]) * char_height2 / (
                        char_height1 + char_height2)
                    y = line_bins[white_region[0]] + offset
                    # y = (line_bins[white_region[0]] + line_bins[white_region[-1]])/2
                    process_cut_lines = True
            white_region = [j]
            last_y = line_bins[j]

        if process_cut_lines and len(line_new_bins) > 0:
            y0 = line_new_bins[-1]
            char_height = y - y0
            height_width_ratio = (char_height * 1.0) / line_width
            ignore_ratio = 0.45

            #if line_chars[char_idx] in [u'三']:
            #    ignore_ratio = 0.55
            if height_width_ratio < ignore_ratio and line_char_lst:
                if j == len(line_bins):
                    line_new_bins.pop()
                    line_new_data.pop()
                    line_new_bins.append(y)
                    line_new_data.append(binary_line_vertical[y])
                    line_char_lst[-1].bottom = y
                pass
            elif height_width_ratio > 1.4 and height_width_ratio < 2.1:  # 2 chars
                #print '2 chars'
                # find cut line between [y0 + char_height / 4, y - char_height / 4]
                cut_y = np.argmin(
                    binary_line_vertical[y0 + char_height / 4: y - char_height / 4 + 1]) + y0 + char_height / 4
                #print 'add cut_y: ', cut_y
                ch = Char(u'', line_left, line_right, line_new_bins[-1], cut_y, line_no,
                          char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                char_idx += 1
                line_new_bins.append(cut_y)
                line_new_data.append(binary_line_vertical[cut_y])

                ch = Char(u'', line_left, line_right, line_new_bins[-1], y, line_no, char_idx + 1,
                          line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                char_idx += 1
                line_new_bins.append(y)
                line_new_data.append(binary_line_vertical[y])
            elif height_width_ratio > 2.1 and height_width_ratio < 2.8:  # 3 chars
                # find cut line
                #print '3 chars'
                cut_y = np.argmin(
                    binary_line_vertical[y0 + char_height / 6: y0 + char_height / 2]) + y0 + char_height / 6
                #print 'add cut_y: ', cut_y
                ch = Char(u'', line_left, line_right, line_new_bins[-1], cut_y, line_no,
                          char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                char_idx += 1
                line_new_bins.append(cut_y)
                line_new_data.append(binary_line_vertical[cut_y])
                cut_y = np.argmin(binary_line_vertical[
                                  y0 + char_height * 3 / 6: y0 + char_height * 5 / 6]) + y0 + char_height * 3 / 6
                #print y, y0, char_height
                #print 'between: ', y0 + char_height * 3 / 6, y0 + char_height * 5 / 6
                #print 'add cut_y: ', cut_y, (y0 + char_height * 3 / 6)
                ch = Char(u'', line_left, line_right, line_new_bins[-1], cut_y, line_no,
                          char_idx + 1, line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                char_idx += 1
                line_new_bins.append(cut_y)
                line_new_data.append(binary_line_vertical[cut_y])
                ch = Char(u'', line_left, line_right, line_new_bins[-1], y, line_no, char_idx + 1,
                          line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                char_idx += 1
                line_new_bins.append(y)
                line_new_data.append(binary_line_vertical[y])
            else:
                ch = Char(u'', line_left, line_right, line_new_bins[-1], y, line_no, char_idx + 1,
                          line_id + u'%02d' % (char_idx + 1))
                line_char_lst.append(ch)
                char_idx += 1
                line_new_bins.append(y)
                line_new_data.append(binary_line_vertical[y])

    remained_count = len(line_chars) - len(line_char_lst)
    for j in range(remained_count):
        # 找到切分图像高度最大的字
        line_char_lst.sort(key=lambda ch: (ch.bottom - ch.top))
        if len(line_char_lst) >= 1:
            last_char = line_char_lst[-1]
            line_char_lst.remove(last_char)
            # 对char_no > last_char.char_no的字调整字符、char_no
            for ch in line_char_lst:
                if ch.char_no > last_char.char_no:
                    ch.char_no = ch.char_no + 1
                    ch.char = line_chars[ch.char_no - 1]
            char_height = last_char.bottom - last_char.top
            #print 'remained cut: ', char_height
            char_idx = last_char.char_no - 1
            char_line_vertical = binary_line_vertical[last_char.top + char_height / 4: last_char.bottom - char_height / 4]
            cut_y = np.argmin(char_line_vertical) + last_char.top + char_height / 4
            #print 'add cut_y: ', cut_y
            line_new_bins.append(cut_y)
            line_new_data.append(binary_line_vertical[cut_y])
            ch = Char(line_chars[char_idx], last_char.left, last_char.right, last_char.top, cut_y, last_char.line_no,
                      char_idx + 1, line_id + u'%02d' % (char_idx + 1))
            line_char_lst.append(ch)
            ch = Char(line_chars[char_idx + 1], last_char.left, last_char.right, cut_y, last_char.bottom, last_char.line_no,
                      char_idx + 2, line_id + u'%02d' % (char_idx + 2))
            line_char_lst.append(ch)

    beyond_count = len(line_char_lst) - len(line_chars)
    #print 'beyond_count: ', beyond_count
    if beyond_count > 0:
        correct_char_lst = []
        short_char_lst = []
        for ch in line_char_lst:
            if ch.height <= 0.65 * line_width:
                short_char_lst.append(ch)
            else:
                correct_char_lst.append(ch)
        #short_char_lst.sort(key=attrgetter('top'))
        #print 'short_char_lst: ', len(short_char_lst)
        short_chars_lst = []
        temp_lst = []
        for ch in short_char_lst:
            if temp_lst:
                if temp_lst[-1].bottom == ch.top:
                    temp_lst.append(ch)
                else:
                    short_chars_lst.append(temp_lst)
                    temp_lst = []
            else:
                temp_lst = [ch]
        if temp_lst:
            short_chars_lst.append(temp_lst)
            temp_lst = []
        for char_lst in short_chars_lst:
            if len(char_lst) > 1:
                if beyond_count > 0:
                    avg_height = (char_lst[-1].bottom - char_lst[0].top) / (len(char_lst) - 1)
                    new_top = char_lst[0].top
                    for i in range(len(char_lst) -1):
                        char_lst[i].set_top_bottom(new_top, new_top + avg_height)
                        new_top = char_lst[i].bottom
                        correct_char_lst.append(char_lst[i])
                    beyond_count = beyond_count - 1
                else:
                    correct_char_lst.extend(char_lst)
            else:
                correct_char_lst.append(char_lst[0])

        line_char_lst = correct_char_lst
    line_char_lst.sort(key=attrgetter('top'))
    last_char_bottom = line_height - 1
    if line_char_lst:
        last_char_bottom = line_char_lst[-1].bottom
    if len(line_char_lst) > len(line_chars):
        line_char_lst = line_char_lst[0:len(line_chars)]
        if line_char_lst:
            line_char_lst[-1].bottom = last_char_bottom
    for i in range(len(line_char_lst)):
        line_char_lst[i].set_char_no(i + 1)
        line_char_lst[i].set_char(line_chars[i])
        line_char_lst[i].set_char_id( line_id + u'%02d' % (i+1) )

    for i in xrange(len(line_char_lst) - 1):
        height1 = line_char_lst[i].bottom - line_char_lst[i].top
        height2 = line_char_lst[i+1].bottom - line_char_lst[i+1].top
        if height1 * 1.0 / height2 > 1.82 or height1 * 1.0 / height2 < 0.55:
            middle = (line_char_lst[i].top + line_char_lst[i+1].bottom) / 2
            line_char_lst[i].bottom = middle
            line_char_lst[i + 1].top = middle

    for ch in line_char_lst:
        ch.cut_char_image(line_image)
        ch.top = ch.top + line_top
        ch.bottom = ch.bottom + line_top
    total_char_lst.extend(line_char_lst)

def process_page(image, text, page_id):
    thresh = filters.threshold_otsu(image)
    binary = (image > thresh).astype('ubyte')
    if len(binary.shape) == 3:
        binary = binary.sum(axis=2) / 3
    binary = 1 - binary
    image_height, image_width = binary.shape

    binary_line = binary.sum(axis=0)

    x_ax = np.arange(1, image_width + 1)
    y_ax = np.arange(1, image_height + 1)

    min_v = binary_line.min()
    max_v = binary_line.max()
    cut_thresh = min_v + (max_v - min_v) / 25
    #print 'min, max, cut_thresh', min_v, max_v, cut_thresh

    bins = []
    data = []
    for i in range(image_width):
        if binary_line[i] <= cut_thresh:
            bins.append(i)
            data.append(binary_line[i])

    new_bins = []
    new_data = []
    last_x = 0
    white_region = []
    for i in range(len(bins)):
        if (bins[i] - last_x) <= 1:
            white_region.append(i)
            last_x = bins[i]
        else:
            #print 'bins[i]: ', bins[i], last_x, white_region
            if len(new_bins) == 0:
                if len(white_region) > 0:
                    #print 'last_x, bins[white_region[-1]]:', bins[white_region[0]], bins[white_region[-1]]
                    x = last_x - (bins[white_region[-1]] - bins[white_region[0]]) / 10
                else:
                    x = last_x
                new_bins.append(x)
                new_data.append(binary_line[x])
            else:
                x = (bins[white_region[0]] + bins[white_region[-1]]) / 2
                new_bins.append(x)
                new_data.append(binary_line[x])
            white_region = [i]
            last_x = bins[i]
    # last white region
    if len(white_region) > 0:
        x = bins[white_region[0]] + (bins[white_region[-1]] - bins[white_region[0]]) / 10
        new_bins.append(x)
        new_data.append(binary_line[x])
        #print 'last white region: ', x

    for i in range(len(new_bins) - 1):
        end_x = new_bins[i+1]
        insert_pos = i + 1
        start_x = new_bins[i]

        while True:
            width = end_x - start_x
            if width >= LINE_WIDTH * 2: # cut
                cut_x = np.argmin(
                    binary_line[start_x + LINE_WIDTH / 2: start_x + LINE_WIDTH * 3 / 2 + 1]) + start_x + LINE_WIDTH / 2
                #print 'add cut_x: ', cut_x
                new_bins.insert(insert_pos, cut_x)
                insert_pos = insert_pos + 1
                start_x = cut_x
            else:
                break

    # char segmentation for each line
    line_texts = text.rstrip().split(u'\n')
    line_texts = filter(lambda x: x != u' ', line_texts)
    line_count = len(line_texts)
    total_char_lst = []

    line_no = 0
    last_x = new_bins[-1]

    line_regions = []
    for i in range(len(new_bins) - 2, -1, -1):
        line_width = last_x - new_bins[i]
        if line_width < 25:
            last_x = new_bins[i]
            continue
        line_image = binary[:, new_bins[i]:last_x]

        binary_line_vertical = line_image.sum(axis=1)
        line_min_v = binary_line_vertical.min()
        line_max_v = binary_line_vertical.max()
        if line_max_v < line_width / 10.0: # 这一行是空白区
            last_x = new_bins[i]
            continue
        line_region = LineRegion(new_bins[i], last_x)
        line_regions.append(line_region)
        last_x = new_bins[i]

    if len(line_regions) - line_count == 1: #如果计算出的行数比文字行数多1
        #print 'line_regions[0].width, line_regions[-1].width:', line_regions[0].width, line_regions[-1].width
        if line_regions[0].width < line_regions[-1].width:
            line_regions.pop(0)
            new_bins.pop()
        else:
            line_regions.pop()
            new_bins.pop(0)

    avg_width = np.average( map(attrgetter('width'), line_regions[1:-2]) )
    print 'avg_width: ', avg_width
    if line_regions[0].width > avg_width * 1.2:
        print 'the width of the first line > avg_width * 1.2'
        line_regions[0].set_right( int(line_regions[0].left + avg_width) )
    if line_regions[-1].width > avg_width * 1.2:
        print 'the width of the last line > avg_width * 1.2'
        line_regions[-1].set_left(int(line_regions[-2].left - avg_width))

    for line_region in line_regions:
        line_no = line_no + 1
        if line_no > line_count:
            break
        line_id = page_id + u'%02dL' % line_no
        #print u'#### line %s: %s ####' % (line_no, line_id)
        line_text = line_texts[line_no - 1]
        if line_text.find(u'<') != -1:  # 这一行有<，表示有小字，不处理
            continue
        space_pos = line_text.find(u';')
        if space_pos != -1:
            line_chars = line_text[space_pos + 1:].strip()
        else:
            line_chars = line_text

        line_image = binary[:, line_region.left: line_region.right]
        binary_line_vertical = line_image.sum(axis=1)
        line_top = 0
        line_bottom = image_height-1
        for j in xrange(image_height):
            if binary_line_vertical[j] > 0:
                break
            line_top = j
        if line_top >= 10:
            line_top = line_top - 10
        else:
            line_top = 0
        for j in xrange(image_height-1, 0, -1):
            if binary_line_vertical[j] > 0:
                break
            line_bottom = j
        if line_bottom <= image_height-11:
            line_bottom = line_bottom + 10
        else:
            line_bottom = image_height-1
        #print 'line_top, line_bottom: ', line_top, line_bottom
        line_image_new = line_image[line_top:line_bottom+1]
        binary_line_vertical_new = binary_line_vertical[line_top:line_bottom+1]

        process_line(line_image_new, binary_line_vertical_new,
                     line_top, line_bottom, line_region.left, line_region.right,
                     line_chars, line_id, line_no, total_char_lst,
                     image_height)
    return total_char_lst
