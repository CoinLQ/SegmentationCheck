from __future__ import absolute_import
from .models import DataPoint
from SegmentationCheck import celery_app as app
from segmentation.models import Character
from django.db.models import Q
from django.db import transaction

@app.task
def calculate_classification_statistics():
    DATA_POINT_NUM = 200
    char_statistics_map = {}
    for ch in Character.objects.filter(~Q(accuracy=-1)):
        range_idx = int(ch.accuracy * DATA_POINT_NUM)
        if range_idx < 0:
            continue
        if range_idx == DATA_POINT_NUM:
            range_idx = DATA_POINT_NUM - 1
        data_point_lst = char_statistics_map.setdefault(ch.char, [0] * DATA_POINT_NUM)
        data_point_lst[range_idx] = data_point_lst[range_idx] + 1
    data_points = []
    for char, data_point_lst in char_statistics_map.iteritems():
        for range_idx in range(DATA_POINT_NUM):
            count = data_point_lst[range_idx]
            data_point = DataPoint(char=char, range_idx=range_idx, count=count)
            data_points.append(data_point)
    with transaction.atomic():
        DataPoint.objects.all().delete()
        DataPoint.objects.bulk_create(data_points)