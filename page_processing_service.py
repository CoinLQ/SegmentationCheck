# coding: utf-8

import skimage.io as io
from page_processing import process_page
import subprocess
import os, sys, redis, logging, cPickle
import traceback

FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(filename='logs/page_processing_service.log', level=logging.INFO, format=FORMAT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Character, Page

redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)

def segment_one_page(page_id, image_name, text):
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
        character_lst.append(character)
    Character.objects.filter(page_id=page_id).delete()
    Character.objects.bulk_create(character_lst)
    #character_data = cPickle.dumps(character)
    #redis_client.rpush('characters', character_data)

def check_if_segment(page_id):
    #cmd = u'ls /home/share/dzj_characters/character_images/%s* 2>/dev/null |head -n1' % page_id
    #output = subprocess.check_output(cmd, shell=True)
    #return (output != '')
    try:
        char = Character.objects.filter(page_id=page_id)[0]
        return False
    except:
        return True

def run_segmentation_loop():
    while True:
        page_data = redis_client.blpop('pages')
        page = cPickle.loads(page_data[1])
        #if not check_if_segment(page.id):
        if True:
            logging.info('page: %s', page.id)
            if page.image:
                try:
                    segment_one_page(page.id, u'/home/share/dzj_characters/page_images/%s' % page.image, page.text)
                except Exception, e:
                    logging.error('exception: %s', e)
                    traceback.print_exc()

if __name__ == '__main__':
    run_segmentation_loop()
