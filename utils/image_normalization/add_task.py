# coding: utf-8
import redis
import sys
import os
import time

sys.path.append('/home/dzj/SegmentationCheck')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Character

redis_client = redis.StrictRedis(host='localhost', port=6379, db=2)
image_list_key = 'seg_classify:image_list'

if __name__ == '__main__':
    count = Character.objects.count()
    iter_count = (count - 1) / 10000
    for i in range(iter_count):
        start = i * 10000
        characters = Character.objects.all()[start: start + 10000]
        for ch in characters:
            char_id = ch.id.encode('utf-8')
            redis_client.rpush(image_list_key, char_id)
        # sleep
        while True:
            list_count = redis_client.llen(image_list_key)
            if list_count > 1000:
                time.sleep(10)
            else:
                break
