import subprocess
import os, sys, redis, logging, cPickle, signal

FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(filename='logs/write_character_service.log', level=logging.INFO, format=FORMAT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SegmentationCheck.settings")
import django
django.setup()
from segmentation.models import Character, Page

redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)

running = True

def handler(signum, frame):
    running = False

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGQUIT, handler)


def run_write_character_loop():
    character_lst = []
    while running:
        character_data = redis_client.blpop('characters')
        character = cPickle.loads(character_data[1])
        logging.info(u'to save character: %s, %s', character.id, character.char)
        character_lst.append(character)
        if len(character_lst) >= 500:
            try:
                Character.objects.bulk_create(character_lst)
                character_lst = []
            except:
                for ch in character_lst:
                    ch.save()
                character_lst = []
    if character_lst:
        try:
            Character.objects.bulk_create(character_lst)
            character_lst = []
        except:
            for ch in character_lst:
                ch.save()
            character_lst = []


if __name__ == '__main__':
    run_write_character_loop()
