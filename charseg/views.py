# -*- coding:utf-8 -*-
from django.http import  JsonResponse
from libs.charseg import charseg
from django.shortcuts import get_object_or_404
from layoutseg.models import Region
from segmentation.models import Page,Character
from django.core import serializers
import json

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
    return JsonResponse(char_lst, safe=False)
