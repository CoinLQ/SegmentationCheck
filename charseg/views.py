# -*- coding:utf-8 -*-
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404
from layoutseg.models import Region
from segmentation.models import Page,Character
from django.core import serializers
import json

from skimage import io
from skimage.exposure import is_low_contrast
from libs.charseg import binarisation
from django.conf import settings
import os
from libs.charseg import charseg
from django.db import connection,transaction

def run_seg(request,pk):
    page = get_object_or_404(Page, pk=pk)
    img_path = page.get_image_path()
    raw_data = serializers.serialize("python",Region.objects.filter(page_id=pk))
    region_lst = [d['fields'] for d in raw_data]
    char_lst = charseg(img_path,region_lst, pk)
    for ch in char_lst:
        char_id = '{0}L{1:02}R{2:02}C{3:03}'.format(pk,ch['line_no'],ch['region_no'],ch['char_no'])
        character = Character(
                id=char_id,
                page_id= pk,
                char=ch['char'],
                left=ch['left'],
                right=ch['right'],
                top=ch['top'],
                bottom=ch['bottom'],
                line_no=ch['line_no'],
                region_no = ch['region_no'],
                char_no=ch['char_no'],
                is_correct=-9 # has not chut char image
                )
        character.save()
#update the CharacterStatistics
    cursor = connection.cursor()
    raw_sql = '''
    INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
    SELECT
        char,
        count(segmentation_character."char") as total_cnt,
        count(segmentation_character."char") as uncheck_cnt,
        0,
        0
    FROM
      public.segmentation_character where page_id='%s'
      group by char
    ON CONFLICT (char)
    DO UPDATE SET
    total_cnt=public.segmentation_characterstatistics.total_cnt + EXCLUDED.total_cnt,
    uncheck_cnt=public.segmentation_characterstatistics.uncheck_cnt + EXCLUDED.uncheck_cnt;
    '''%(pk)
    cursor.execute(raw_sql)
    return JsonResponse(char_lst, safe=False)


def cutchar(page_img_path,char_lst,page_id):
    image = io.imread(page_img_path, 0)
    binary = binarisation(image)
    binary_image = (binary * 255).astype('ubyte')
    char_dir = settings.CHARACTER_IMAGE_ROOT+ page_id+'/'
    if not os.path.exists(char_dir):
        os.makedirs(char_dir)
    #char = char_lst[0]
    for char in char_lst:
        char_image = binary_image[char.top:char.bottom,char.left:char.right]
        char_filename = char.id+'.png'
        char_path = char_dir+char_filename
        try:
            io.imsave(char_path, char_image)
            status = 0
            if is_low_contrast(char_image):
                status = -5
        except:
            char_filename = ''
            status = -6
        char.is_correct = status
        char.image = char_filename
        char.save()

def run_cut(request,pk):
    page = get_object_or_404(Page, pk=pk)
    page_img_path = page.get_image_path()
    char_lst = Character.objects.filter(page_id=pk)
    cutchar(page_img_path,char_lst,pk)
    data = {'status': 'ok'}
    return JsonResponse(data, safe=False)

