#!/usr/bin/python
# -*- coding: utf-8 -*-
from celery import task
from django.db import connection
from django.db.models import Q
from segmentation.models import Character, CharacterStatistics
from .models import ClassificationTask, ClassificationCompareResult
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
from sklearn.linear_model import LogisticRegressionCV
import time
from itertools import chain

from utils.image_normalization.normalization import normalize
from utils.to_slack import push_to_slack
from thinning import convert_image, thinning
import cPickle
import numpy as np
import traceback
import random
from datetime import datetime
from operator import itemgetter
# import the logging library
import logging

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

@task
def classify_with_random_samples(char, positive_sample_count, auto_apply=False, random_sample=0):
    print char, positive_sample_count
    started = datetime.now()
    start_time = time.time()
    query = Character.objects.filter(char=char)
    positive_samples, negative_samples, test_X, test_y, test_char_id_lst, test_accuracy_lst = \
        prepare_data_with_database2(query)
    X = []
    y = []
    if random_sample != 0:
        if positive_sample_count > 0:
            if len(positive_samples) > positive_sample_count:
                positive_samples = random.sample(positive_samples, positive_sample_count)
            if len(negative_samples) > positive_sample_count:
                negative_samples = random.sample(negative_samples, positive_sample_count)
    else:
        if len(positive_samples) > positive_sample_count:
            positive_samples.sort(key=itemgetter(2), reverse=True)
            positive_samples = positive_samples[:positive_sample_count]
        if len(negative_samples) > positive_sample_count:
            negative_samples.sort(key=itemgetter(2))
            negative_samples = negative_samples[:positive_sample_count]
    for sample in positive_samples:
        X.append(sample[0])
        y.append(sample[1])
    for sample in negative_samples:
        X.append(sample[0])
        y.append(sample[1])
    train_count = len(y)
    predict_count = len(test_y)
    if 1 == len(set(y)) or train_count < 10 or predict_count == 0:
        return
    fetch_spent = int(time.time() - start_time)
    print "fetch data done, spent %s seconds." % fetch_spent
    start_time = time.time()
    print "traning: data size: %d" % len(y)
    model = LogisticRegressionCV(cv=5, solver='liblinear', n_jobs=1)
    try:
        model.fit(X, y)
        training_spent = int(time.time() - start_time)
        print "training done, spent %s seconds." % training_spent
        # print 'params: '
        # for k, v in model.get_params().iteritems():
        #    print '\t', k, ' : ', v
        print 'score: ', model.score(X, y)
    except Exception, e:
        print 'except: ', e
        traceback.print_exc()
        return
    start_time = time.time()
    print "predict: data size: %d" % len(test_X)
    predicted = model.predict_proba(test_X)
    #predicted = map(lambda x: x[1], predicted)
    predict_spent = int(time.time() - start_time)
    print "predict done, spent %s seconds." % predict_spent
    completed = datetime.now()
    task = ClassificationTask.create(char, u'', train_count, predict_count,
                                     started, completed, fetch_spent, training_spent, predict_spent, auto_apply)
    task.save()
    compare_results = []
    results = []
    for i in range(predict_count):
        new_accuracy = int(predicted[i][1] * 1000)
        origin_accuracy = test_accuracy_lst[i]
        difference = new_accuracy - origin_accuracy
        results.append( (test_char_id_lst[i], origin_accuracy, new_accuracy, difference) )
    results.sort(key=itemgetter(3), reverse=True)
    # selected_count = max(predict_count/10, 1000)
    selected_count = max(predict_count/2, 1000)
    for char_id, origin_accuracy, new_accuracy, difference in results[:selected_count]:
        if difference != 0:
            result = ClassificationCompareResult.create(task, char_id, origin_accuracy, new_accuracy)
            compare_results.append(result)
    if len(compare_results) > 0:
        ClassificationCompareResult.objects.bulk_create(compare_results)
    if auto_apply:
        task.update_result()


# @task
def classify(_char):
    print 'to fetch data'
    start_time = time.time()
    char_count = Character.objects.filter(char=_char, is_correct=1).count()
    if char_count < 10:
        return
    char_lst = Character.objects.filter(char=_char)
    y, X, ty, tX, t_charid_lst, test_accuracy_lst = prepare_data_with_database(char_lst)
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
    test_accuracy_lst = []
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
            test_accuracy_lst.append(char.accuracy)
            if abs(label) == 1:
                prob_x.append(feature_vector)
                prob_y.append(label)
    return (prob_y, prob_x, test_y, test_x, test_char_id_lst, test_accuracy_lst)

def prepare_data_with_database2(char_lst):
    positive_samples = []
    negative_samples = []
    test_x = []
    test_y = []
    test_char_id_lst = []
    test_accuracy_lst = []
    logger = logging.getLogger()

    for char in char_lst:
        label = char.is_correct
        img_path = char.get_image_path()
        char_id = char.id
        try:
            binary = normalize(img_path)
            feature_vector = binary.ravel()
        except Exception, e:
            #push_to_slack(msg)
            # Get an instance of a logger
            msg = "ID: %s  %s feature_vector fetch failure!" % (char.id, char.char)
            logger.error(e)
            logger.error(msg)
            feature_vector = None
        if feature_vector is not None:
            test_x.append(feature_vector)
            test_y.append( int(label) )
            test_char_id_lst.append(char_id)
            test_accuracy_lst.append(char.accuracy)
            if label == 1:
                positive_samples.append([feature_vector, label, char.accuracy])
            elif label == -1:
                negative_samples.append([feature_vector, label, char.accuracy])
    return (positive_samples, negative_samples, test_x, test_y, test_char_id_lst, test_accuracy_lst)

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
