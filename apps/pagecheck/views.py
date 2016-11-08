# -*- coding:utf-8 -*-
from django.shortcuts import render
from segmentation.models import Page, Character,CharacterStatistics
from django.views import generic

class PageCheckView(generic.ListView):
    template_name = 'pagecheck/page_check.html'
    def get_queryset(self):
        pk = self.kwargs['pk']
        #only show the page had been segment(right field is not equal 0),and had not been check
        return Page.objects.filter(id__startswith=pk).exclude(right=0).filter(is_correct=0)[:9]
        #return Page.objects.filter(id='LQ-V00001P00001B1')

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageCheckView, self).dispatch(*args, **kwargs)

#@login_required(login_url='/account/login/')
def set_page_correct(request):
    if 'id' in request.POST:
        page_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        page = Page.objects.get(id = page_id)
        page.is_correct = is_correct
        page.save()
        if is_correct == -4 or is_correct == -3:#页面错误
            Character.objects.filter(page_id = page_id).update(is_correct=is_correct)
#update the CharacterStatistics
            cursor = connection.cursor()
            raw_sql = '''
            INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
            SELECT
                char,
                0,
                0,
                count(segmentation_character."char") as err_cnt,
                0
            FROM
              public.segmentation_character where page_id='%s'
              group by char
            ON CONFLICT (char)
            DO UPDATE SET
            uncheck_cnt=public.segmentation_characterstatistics.uncheck_cnt - EXCLUDED.err_cnt,
            err_cnt=public.segmentation_characterstatistics.err_cnt + EXCLUDED.err_cnt;
            '''%(page_id)
            print raw_sql
            cursor.execute(raw_sql)
        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

