# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from segmentation.models import Character, CharacterStatistics
from django.views import generic
import random
from django.db.models import F
from utils.get_checked_character import get_checked_character
import datetime
from django.contrib.auth.decorators import user_passes_test


class CharacterIndex(generic.ListView):
    model = CharacterStatistics


def index(request):
    char_cnt_lst = CharacterStatistics.objects.all().order_by('-total_cnt')[:20]
    return render(request, 'characters/character_index.html', {'characterstatistics_list': char_cnt_lst})

@user_passes_test(lambda u:u.is_staff, login_url='/quiz')
def task(request):
    today = datetime.datetime.now().strftime("%Y%m%d")
    checkin_date = request.session.get('checkin_date', 0)
    if checkin_date != today:
        request.session['check_char_number'] = 0
        request.session['checkin_date'] = today
    check_char_number = request.session.get('check_char_number',0)
    #char_lst = CharacterStatistics.objects.filter(uncheck_cnt__gt=0).order_by('-total_cnt')[:30]
    #char = random.choice(char_lst)
    char = get_checked_character()
    return render(request,'characters/characters.html',{'char':char,'check_char_number':check_char_number} )


# @login_required(login_url='/segmentation/login/')
def set_correct(request):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        char = request.POST['char']
        char.encode('utf-8')
        if Character.objects.filter(id=char_id).filter(is_correct=0).exists():
            CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=F('uncheck_cnt')-1)
        Character.objects.filter(id=char_id).update(is_correct=is_correct)
        CharacterStatistics.objects.filter(char=char).update(err_cnt=F('err_cnt')-is_correct)
        data = {'status': 'ok'}
    elif 'charArr[]' in request.POST:
        check_char_number = request.session.get('check_char_number',0)
        request.session['check_char_number'] = check_char_number+1
        charArr = request.POST.getlist('charArr[]')
        char = request.POST['char']
        updateNum = int(request.POST['updateNum'])
        Character.objects.filter(id__in = charArr ).filter(is_correct=0).update(is_correct=1)
        CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=F('uncheck_cnt')-updateNum)
        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)
