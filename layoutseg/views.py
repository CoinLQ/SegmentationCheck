# -*- coding:utf-8 -*-
from django.http import  JsonResponse
from libs.layoutseg import layout_seg
from django.shortcuts import get_object_or_404
from segmentation.models import Page
from layoutseg.models import Region

def run_seg(request,pk):
    page = get_object_or_404(Page, pk=pk)
    img_path = page.get_image_path()
    text = page.text
    region_lst = layout_seg(img_path, text)
    for region in region_lst:
        region_id = '{0}l{1:02}r{2:02}'.format(pk,region['line_no'],region['region_no'])
        _region = Region(
                id = region_id,
                page_id=pk,
                text=region['text'],
                left=region['left'],
                right=region['right'],
                top=region['top'],
                bottom=region['bottom'],
                line_no=region['line_no'],
                region_no=region['region_no'],
                )
        if u'mark' in region:
            _region.mark = region['mark']
        _region.save()
    return JsonResponse(region_lst, safe=False)
