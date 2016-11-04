# coding: utf-8
import cPickle
import numpy as np
import os

import skimage.io as io
import skimage.filters as filters
import sys
import redis
from  normalization import nln

redis_client = redis.StrictRedis(host='localhost', port=6379, db=2)
image_list_key = 'seg_classify:image_list'


def normalize_image(char_id):
    page_id = char_id[:-5]
    img_path = '/data/share/dzj_characters/character_images/%s/%s.jpg' % (page_id, char_id)
    nln_path = '/data/share/dzj_characters/character_images/npy/character_images/%s/%s.nln.npy' % (page_id, char_id)
    x = None
    if not os.path.exists(nln_path):
        if not os.path.isfile(img_path):
            print 'no img: %s' % char_id
            return
        try:
            binary = nln(img_path)
            x = binary.ravel()
            if x is not None:
                np.save(nln_path, x)
                #print 'save %s' % char_id
        except Exception, e:
            print 'except %s: %s' % (char_id, e)

if __name__ == '__main__':
    while True:
        char_id = redis_client.blpop(image_list_key)
        if char_id:
            normalize_image(char_id[1])