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

    cur.execute("select char, count(*) from segmentation_character where is_correct=0 or is_correct<-10 or is_correct>10 group by char;")
    results = cur.fetchall()
    remained_characters = [r[0] for r in results]

    char_correct_map_lst = [{}, {}]
    is_correct_values = [1, -1]
    for i in range(2):
        is_correct = is_correct_values[i]
        cur.execute("select char, count(*) from segmentation_character where is_correct=%s group by char;",
                    (is_correct,))
        results = cur.fetchall()

        for r in results:
            char_correct_map_lst[i][r[0]] = r[1]
    cur.close()
    conn.close()

    selected_character_lst = []
    for char, count in char_count_map.iteritems():
        if char in remained_characters and \
                (char not in char_correct_map_lst[0] or char not in char_correct_map_lst[1] or \
                             char_correct_map_lst[0][char] < 50 or char_correct_map_lst[1][char] < 50)\
                and char_count_map[char] > 5:

            selected_character_lst.append( (char, count) )

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
        if all_count != 0:
            index = random.randint(0, all_count-1)
            char = redis_client.lindex(all_characters_key, index)
            return char.decode('utf-8')
        else:
            return u'无'
    if index >= count:
        redis_client.set(characters_index_key, 0)
        index = 0
    char = redis_client.lindex(characters_key, index)
    return char.decode('utf-8')

if __name__ == '__main__':
    main()
