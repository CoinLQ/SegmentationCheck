#!/usr/bin/python
# -*- coding: utf-8 -*-
from celery import task
from django.db import connection
from django.db.models import Q
from segmentation.models import Character, CharacterStatistics
import sys
import os
from scipy.misc import imresize  # for image resize
from skimage import io
from skimage.color import rgb2gray, gray2rgb

from skimage.filters import threshold_otsu
# sys.path.append('/home/can/PycharmProjects/imageprocess/libsvm/python')
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
import time
from itertools import chain

from utils.image_normalization.normalization import normalize
from thinning import convert_image, thinning
import cPickle
import numpy as np
import traceback

# @task
def add(x, y):
    return x + y


# @task
def update_char_stastics():
    cursor = connection.cursor()
    raw_sql = '''
    INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
    SELECT
        char,
        count(segmentation_character."char") as total_cnt,
        sum(case when is_correct= 0 then 1 else 0 end) as uncheck_cnt,
        sum(case when is_correct<0 then 1 else 0 end) as err_cnt,
        0
    FROM
      public.segmentation_character
      group by char
    ON CONFLICT (char)
    DO UPDATE SET
    total_cnt=EXCLUDED.total_cnt,
    uncheck_cnt=EXCLUDED.uncheck_cnt,
    err_cnt =EXCLUDED.err_cnt;
    '''
    cursor.execute(raw_sql)
    return 'update CharacterStatistics'


# @task
def classify(_char):
    print 'to fetch data'
    start_time = time.time()
    char_count = Character.objects.filter(char=_char, is_correct=1).count()
    if char_count < 10:
        return
    char_lst = Character.objects.filter(char=_char)
    y, X, ty, tX, t_charid_lst = prepare_data_with_database(char_lst)
    if len(y) == 0 or len(ty) == 0:
        return
    if 1 == len(set(y)) or len(y) < 10:
        return
    fetch_negative_samples(_char, X, y)
    if len(y) == 0 or len(ty) == 0:
        return
    if 1 == len(set(y)) or len(y) < 50:
        return

    print "fetch data done, spent %s seconds." % int(time.time() - start_time)
    start_time = time.time()
    print "traning: data size: %d" % len(y)
    from sklearn.linear_model import LogisticRegressionCV
    model = LogisticRegressionCV(cv=5, solver='liblinear', n_jobs=1)
    try:
        model.fit(X, y)
        print "training done, spent %s seconds." % int(time.time() - start_time)
        #print 'params: '
        #for k, v in model.get_params().iteritems():
        #    print '\t', k, ' : ', v
        print 'score: ', model.score(X, y)
    except Exception, e:
        print 'except: ', e
        traceback.print_exc()
        return
    #print "----model------"
    # make predictions
    # expected = y
    # predicted = model.predict(X)
    # summarize the fit of the model
    '''
    print "-----make predictions-----"
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    '''
    if len(tX) == 0:
        return
    start_time = time.time()
    print "predict: data size: %d" % len(tX)
    predicted = model.predict_proba(tX)
    predicted = map(lambda x: x[1], predicted)
    print "predict done, spent %s seconds." % int(time.time() - start_time)
    output_result2sql(predicted, t_charid_lst, _char)
    print "output done."

def prepare_data_with_database(char_lst):
    prob_x = []
    prob_y = []
    test_x = []
    test_y = []
    test_char_id_lst = []
    for char in char_lst:
        label = char.is_correct
        img_path = char.get_image_path()
        char_id = char.id
        try:
            binary = normalize(img_path)
            feature_vector = binary.ravel()
        except:
            feature_vector = None
        if feature_vector is not None:
            test_x.append(feature_vector)
            test_y.append( int(label) )
            test_char_id_lst.append(char_id)
            if abs(label) == 1:
                prob_x.append(feature_vector)
                prob_y.append(label)
    return (prob_y, prob_x, test_y, test_x, test_char_id_lst)

def fetch_negative_samples(char, X = [] * 1, y = [] * 1):
    char_count_map = {}
    total_count = Character.objects.filter(Q(is_correct=1) & ~Q(char=char)).count()
    print 'negative samples: total %d' % total_count
    iter_count = (total_count - 1) / 10000
    for i in range(iter_count):
        start = i * 10000
        characters = Character.objects.filter(Q(is_correct=1) & ~Q(char=char))[start:start+10000]
        for ch in characters:
            count = char_count_map.get(ch.char, 0)
            if count >= 5:
                continue
            label = -1
            img_path = ch.get_image_path()
            try:
                binary = normalize(img_path)
                feature_vector = binary.ravel()
            except:
                feature_vector = None
            if feature_vector is not None:
                X.append(feature_vector)
                y.append( label )
                char_count_map[ch.char] = count + 1
    return X, y


def output_result2sql(p_labels, t_charid_lst, char):
    result_file = '/home/dzj/classification_results/%s_result_char.sql' % char.encode('utf-8')
    with open(result_file, 'w+') as res_f:
        # length = [len(p_labels),2000][len(p_labels)>2000]
        length = len(p_labels)
        for i in range(length):
            update_sql = "update segmentation_character set accuracy = %g where id = '%s';\n"\
                         % (int(p_labels[i]*1000), t_charid_lst[i])
            res_f.write(update_sql)
