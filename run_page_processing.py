# coding: utf-8

import skimage.io as io
from page_processing import process_page
import subprocess
#import os, sys, redis
import os, sys
import cPickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Character, Page

text1 = u''
def test_file():
    vol_no = u'01'
    page_no = u'001'
    output = subprocess.check_output(
        'cd /media/DATA/work/image-preprocessing/binary_image/%s/%s/; ls *.txt 2>/dev/null' % (vol_no, page_no),
        shell=True)
    pos = output.find('.txt')
    if pos == -1:
        sys.exit(-1)
    page_id_prefix = output[:pos - 1]
    page_id = page_id_prefix + 'a'
    image_name = u'/media/DATA/work/image-preprocessing/binary_image/%s/%s/%s.jpg' % (vol_no, page_no, page_id)
    text_name = u'/media/DATA/work/image-preprocessing/binary_image/%s/%s/%s.txt' % (vol_no, page_no, page_id)
    image = io.imread(image_name, 0)
    # image = io.imread(u'/home/xianbu/custom/1a.jpg', 0)
    text = u''
    with open(text_name, 'r') as f:
        text = f.read().decode('utf-8')
        text1 = text
    process_page(image, text, page_id)
    total_char_lst = process_page(image, text, page_id)

    import django
    django.setup()
    from segmentation.models import Character

    character_lst = []
    for ch in total_char_lst:
        character = Character(id=ch.char_id.strip(), page_id=page_id, char=ch.char,
                              image=ch.char_id.strip() + u'.jpg',
                              left=ch.left, right=ch.right,
                              top=ch.top, bottom=ch.bottom,
                              line_no=ch.line_no, char_no=ch.char_no,
                              is_correct=False)
        #character_lst.append(character)
        print character
        character.save()
    #Character.objects.bulk_create(character_lst)

def segment_one_page(page_id, image_name, text):
    if text == text1:
        print 'equal----'
    image = io.imread(image_name, 0)
    total_char_lst = process_page(image, text, page_id)
    character_lst = []
    for ch in total_char_lst:
        character = Character(id=ch.char_id.strip(), page_id=page_id, char=ch.char,
                              image=ch.char_id.strip() + u'.jpg',
                              left=ch.left, right=ch.right,
                              top=ch.top, bottom=ch.bottom,
                              line_no=ch.line_no, char_no=ch.char_no,
                              is_correct=False)
        #character_lst.append(character)
        print character
        character.save()
        #Character.objects.bulk_create(character_lst)

def check_if_segment(page_id):
    cmd = u'ls /home/share/dzj_characters/character_images/%s* 2>/dev/null |head -n1' % page_id
    output = subprocess.check_output(cmd, shell=True)
    return (output != '')

def run_segmentation_for_all_pages():
    iter = Page.objects.iterator()
    for page in iter:
        if check_if_segment(page.id):
            continue
        print 'page.id: ', page.id.encode('utf-8')
        segment_one_page(page.id, u'/home/share/dzj_characters/page_images/%s' % page.image, page.text)

def add_segmentation_task():
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)
    iter = Page.objects.iterator()
    for page in iter:
        print page.id
        page_data = cPickle.dumps(page)
        redis_client.rpush('pages', page_data)

if __name__ == '__main__':
    #test_file()
    run_segmentation_for_all_pages()
    #add_segmentation_task()
