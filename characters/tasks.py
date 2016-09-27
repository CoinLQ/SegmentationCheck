#!/usr/bin/python
# -*- coding: utf-8 -*-
from celery import task
from django.db import connection
from segmentation.models import Character, CharacterStatistics
import sys
import os
from scipy.misc import imresize  # for image resize
from skimage import io
from skimage.color import rgb2gray, gray2rgb

from skimage.filter import threshold_otsu
# sys.path.append('/home/can/PycharmProjects/imageprocess/libsvm/python')
from sklearn import preprocessing
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier


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
def classify():
    # char_info = CharacterStatistics.objects.all().filter
    _char = u'不'
    char_lst = Character.objects.filter(char=_char)
    y, X, ty, tX, t_charid_lst = prepare_data_with_database(char_lst)

    print "traning"
    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    # standardize the data attributes
    standardized_X = preprocessing.scale(X)

    model = ExtraTreesClassifier()
    model.fit(X, y)
    # display the relative importance of each attribute
    print "=============feature_importances_========"
    print(model.feature_importances_)

    print "==LogisticRegression=="
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    model.fit(X, y)
    print "----model------"
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print "-----make predictions-----"
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    predicted = model.predict(tX)
    output_result2sql(predicted, t_charid_lst, _char)
    return 'classify'


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
        if not os.path.exists(img_path):
            continue
        src_image = io.imread(img_path, 0)
        img_gray = rgb2gray(src_image)
        img_resize = imresize(img_gray, [10, 15], 'nearest')
        try:
            thresh = threshold_otsu(img_resize)
        except:
            continue
        binary = img_resize > thresh
        im = (binary * 1).astype('ubyte')
        im.shape = 1, -1
        x = im.tolist()
        if int(label) == 0:
            test_x += x
            test_y += [int(label)]
            # test_path += [img_path]
            test_char_id_lst += [char_id]
        else:
            if int(label) < 0:
                label = -1
            elif int(label) > 0:
                label = 1
            prob_x += x
            prob_y += [label]
    # return (prob_y, prob_x, test_y, test_x, test_path)
    return (prob_y, prob_x, test_y, test_x, test_char_id_lst)


def output_result2sql(p_labels, t_charid_lst, char):
    result_file = char+'result_char.sql'
    with open(result_file, 'w+') as res_f:
        # length = [len(p_labels),2000][len(p_labels)>2000]
        length = len(p_labels)
        for i in range(length):
            update_sql = "update segmentation_character set is_correct = %d \
            where id = '%s';" % p_labels[i], t_charid_lst[i]
            res_f.write(update_sql)
