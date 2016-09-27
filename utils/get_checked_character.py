# coding: utf-8
import psycopg2
from operator import itemgetter
import redis
import random

redis_client = redis.StrictRedis(host='localhost', port=6379, db=2)
characters_key = 'seg_web:selected_characters'
characters_index_key = 'seg_web:selected_characters_index'
all_characters_key = 'seg_web:all_characters'

def main():
    conn = psycopg2.connect("dbname=dzj_characters user=dzj password=dzjsql")
    cur = conn.cursor()
    char_count_map = {}
    cur.execute("select char, count(*) from segmentation_character group by char;")
    results = cur.fetchall()
    redis_client.delete(all_characters_key)
    for r in results:
        char_count_map[r[0]] = r[1]
        redis_client.rpush(all_characters_key, r[0])
    selected_characters = {}
    for i in [1, -1]:
        cur.execute("select char, count(*) from segmentation_character where is_correct=%s group by char;", (i,))
        results = cur.fetchall()
        for r in results:
            if r[1] < 50:
                selected_characters[r[0]] = char_count_map[r[0]]
    cur.close()
    conn.close()
    selected_character_lst = selected_characters.items()
    selected_character_lst.sort(key=itemgetter(1), reverse=True)

    redis_client.delete(characters_key)
    for c in selected_character_lst:
        redis_client.rpush(characters_key, c[0])
    redis_client.set(characters_index_key, -1)

def get_checked_character():
    '''
    :return: 下一个要检查的字
    '''
    index = redis_client.incr(characters_index_key)
    count = redis_client.llen(characters_key)
    if count == 0:
        redis_client.set(characters_index_key, -1)
        all_count = redis_client.llen(all_characters_key)
        index = random.randint(0, all_count-1)
        char = redis_client.lindex(all_characters_key, index)
        return char.decode('utf-8')
    if index >= count:
        redis_client.set(characters_index_key, 0)
        index = 0
    char = redis_client.lindex(characters_key, index)
    return char.decode('utf-8')

if __name__ == '__main__':
    main()
