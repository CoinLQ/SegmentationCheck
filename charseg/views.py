# -*- coding:utf-8 -*-
from django.http import  JsonResponse
from libs.charseg import charseg
from django.shortcuts import get_object_or_404
from layoutseg.models import Region
from segmentation.models import Page
from django.core import serializers
import json

def run_seg(request,pk):
    page = get_object_or_404(Page, pk=pk)
    img_path = page.get_image_path()

    raw_data = serializers.serialize("python",Region.objects.filter(page_id=pk))
    region_lst = [d['fields'] for d in raw_data]
    char_lst = charseg(img_path,region_lst, pk)
    return JsonResponse(char_lst, safe=False)
