# coding: utf-8
import os
from operator import itemgetter
import redis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from django.db import connection
from characters.tasks import classify

redis_client = redis.StrictRedis(host='localhost', port=6379, db=2)
characters_key = 'seg_web:classified_character_count'

def main():
    results = []
    with connection.cursor() as cursor:
        cursor.execute("select char, count(is_correct=1) as correct_cnt, count(is_correct=-1) as err_cnt from \
        segmentation_character group by char;")
        results = cursor.fetchall()
    if len(results) > 0:
        results.sort(key=itemgetter(1), reverse=True)
        character_count_map = redis_client.hgetall(characters_key)

        for r in results:
            ch = r[0].encode('utf-8')
            count_limit = character_count_map.get(ch, 50)
            count_limit = int(count_limit)
            if r[1] < count_limit and r[2] < 1:
                continue
            new_count_limit = r[1] + 50
            redis_client.hset(characters_key, r[0], new_count_limit)
            # r[0]
            print r[0]
            classify(r[0])

if __name__ == '__main__':
    main()
