# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from segmentation.models import Character, CharacterStatistics
from django.db.models import F
from utils.get_checked_character import get_checked_character
import datetime
from django.contrib.auth.decorators import user_passes_test
from .models import UserCredit
import redis
from django.views import generic
from django.core.cache import cache
from libs.fetch_variants import fetcher
import json
import random

class Index(generic.ListView):
    template_name = 'characters/char_manage.html'
    def get_queryset(self):
        char_lst = cache.get('characterstatistics_lst', None)
        if char_lst is None:
            print 'no cache'
            char_lst = CharacterStatistics.objects.all().order_by('-total_cnt','char')
            cache.set('characterstatistics_lst', char_lst)
        return  char_lst

def index(request):
    return render(request, 'characters/character_index.html')

def help(request):
    return render(request, 'characters/characters_help.html')

#@user_passes_test(lambda u:u.is_staff, login_url='/quiz')
def task(request):
    # redis_client = redis.StrictRedis(host='localhost', port=6379, db=2)
    # all_characters_key = 'seg_web:all_characters'
    # selected_characters = 'seg_web:selected_characters'
    # stage_characters = 'seg_web:stage_characters'

    # total_cnt = redis_client.get(stage_characters)
    # select_cnt = redis_client.llen(selected_characters)
    # done_cnt = total_cnt - select_cnt
    query = CharacterStatistics.objects.filter(total_cnt__lte=5,total_cnt__gt=0)
    total_cnt = query.count()
    select_cnt = query.filter(uncheck_cnt__gt=0).count()
    done_cnt = total_cnt - select_cnt

    today = datetime.datetime.now().strftime("%Y%m%d")
    checkin_date = request.session.get('checkin_date', 0)
    if checkin_date != today:
        #active_date=time.strptime(checkin_date,'%Y%m%d')
        check_char_number = request.session.get('check_char_number', 0)
        if check_char_number !=0:
            user_credit = UserCredit(user=request.user,
                                     active_date=checkin_date,
                                     credit=request.session['check_char_number'],
                                     username=request.user.username
                                     )
            user_credit.save()
        request.session['check_char_number'] = 0
        request.session['checkin_date'] = today
    check_char_number = request.session.get('check_char_number',0)
    char_lst = query.filter(uncheck_cnt__gt=0).order_by('-total_cnt')[:30]
    if char_lst:
        char = random.choice(char_lst).char
    else:
        char = u'无'
    #char = get_checked_character()
    #lq_variant = fetcher.fetch_variants(u'麤')
    lq_variant = ''
    return render(request,'characters/characters.html',{'char':char,
                                                        'check_char_number':check_char_number,
                                                        'done_cnt':done_cnt,
                                                        'total_cnt':total_cnt,
                                                        'variant_lst':lq_variant,
                                                        } )


# @login_required(login_url='/segmentation/login/')
def set_correct(request):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        char = request.POST['char']
        char.encode('utf-8')
        if Character.objects.filter(id=char_id).filter(is_correct=0).exists():  # uncheck -> check
            if 1 == is_correct:
                CharacterStatistics.objects.filter(char=char).\
                    update(uncheck_cnt=F('uncheck_cnt')-1, correct_cnt=F('correct_cnt')+1)
            else:
                CharacterStatistics.objects.filter(char=char).\
                    update(uncheck_cnt=F('uncheck_cnt')-1, err_cnt=F('err_cnt')+1)
        else:  # correct <-> err  in check
            CharacterStatistics.objects.filter(char=char).\
                update(err_cnt=F('err_cnt')-is_correct, correct_cnt=F('correct_cnt')+is_correct)
        Character.objects.filter(id=char_id).update(is_correct=is_correct)
        data = {'status': 'ok'}
    elif (('e_charArr[]' in request.POST) or ('c_charArr[]' in request.POST)): # uncheck -> check
        check_char_number = request.session.get('check_char_number',0)
        request.session['check_char_number'] = check_char_number+1
        charArr = request.POST.getlist('e_charArr[]')
        char = request.POST['char']
        if charArr:
            updateNum = Character.objects.filter(id__in =charArr).update(is_correct=-1)
            CharacterStatistics.objects.filter(char=char). \
                    update(uncheck_cnt=F('uncheck_cnt')-updateNum, err_cnt=F('err_cnt')+updateNum)

        charArr = request.POST.getlist('c_charArr[]')
        if charArr:
            updateNum = Character.objects.filter(id__in =charArr).update(is_correct=1)
            CharacterStatistics.objects.filter(char=char).\
                    update(uncheck_cnt=F('uncheck_cnt')-updateNum, correct_cnt=F('correct_cnt')+updateNum)

        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

def tree_map(request):
    return render(request, 'characters/tree_map.html')

def get_marked_char_count(request):
    out_lst = cache.get('marked_char_count', None)
    if out_lst is None:
        sql = u'SELECT char, \
        count(CASE WHEN is_correct=1 THEN 1 END) as mark_correct_by_man, \
        count(CASE WHEN is_correct=-1 THEN 1 END) as mark_wrong_by_man, \
        count(CASE WHEN is_correct=0 and accuracy>0.5 THEN 1 END) as mark_correct_by_pc, \
        count(CASE WHEN is_correct=0 and accuracy<0.5 THEN 1 END) as mark_wrong_by_pc \
    FROM segmentation_character GROUP BY char;'
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        out_lst = []
        for r in results:
            d = {
                u'char': r[0],
                u'mark_correct_by_man': r[1],
                u'mark_wrong_by_man': r[2],
                u'mark_correct_by_pc': r[3],
                u'mark_wrong_by_pc': r[4],
            }
            out_lst.append(d)
        cache.set('marked_char_count', out_lst)
    return JsonResponse({'status': 'ok', 'data': out_lst})

'''
def variant(request):
    lq_variant = fetcher.fetch_variants(u'麤')
    data = {'variant_lst':lq_variant}
    return  JsonResponse(data)
'''
