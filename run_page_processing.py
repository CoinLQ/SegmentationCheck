# coding: utf-8

import skimage.io as io
from page_processing import process_page

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")

def test_file():
    page_id = u'K0001V01P0425a'
    #page_id = u'K0001V01P0425b'
    #page_id = u'K0001V01P0425c'
    image = io.imread(u'/home/share/dzj_characters/pages/%s.jpg' % page_id, 0)
    text = u''
    with open(u'/home/xianbu/custom/%s.txt' % page_id, 'r') as f:
        text = f.read().decode('utf-8')
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
        character_lst.append(character)
        character.save()
    #Character.objects.bulk_create(character_lst)


if __name__ == '__main__':
    test_file()