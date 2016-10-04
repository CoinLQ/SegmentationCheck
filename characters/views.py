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
from libs.fetch_variants import fetcher


class Index(generic.ListView):
    #model = CharacterStatistics
    template_name = 'characters/char_manage.html'
    def get_queryset(self):
        return CharacterStatistics.objects.all().order_by('-total_cnt','char')

def index(request):
    return render(request, 'characters/character_index.html')

@user_passes_test(lambda u:u.is_staff, login_url='/quiz')
def task(request):
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=2)
    all_characters_key = 'seg_web:all_characters'
    selected_characters = 'seg_web:selected_characters'

    total_cnt = redis_client.llen(all_characters_key)
    select_cnt = redis_client.llen(selected_characters)
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
    #char_lst = CharacterStatistics.objects.filter(uncheck_cnt__gt=0).order_by('-total_cnt')[:30]
    #char = random.choice(char_lst)
    char = get_checked_character()
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
    elif 'charArr[]' in request.POST: # uncheck -> check
        check_char_number = request.session.get('check_char_number',0)
        request.session['check_char_number'] = check_char_number+1
        charArr = request.POST.getlist('charArr[]')
        char = request.POST['char']
        is_correct = int(request.POST['is_correct'])
        #updateNum = int(request.POST['updateNum'])
        updateNum = Character.objects.filter(id__in =charArr).filter(is_correct=0).update(is_correct=is_correct) #TODO remove filter
        if is_correct == 1:
            CharacterStatistics.objects.filter(char=char).\
                update(uncheck_cnt=F('uncheck_cnt')-updateNum, correct_cnt=F('correct_cnt')+updateNum)
        else:
            CharacterStatistics.objects.filter(char=char). \
                update(uncheck_cnt=F('uncheck_cnt')-updateNum, err_cnt=F('err_cnt')+updateNum)
        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)
'''
def variant(request):
    lq_variant = fetcher.fetch_variants(u'麤')
    data = {'variant_lst':lq_variant}
    return  JsonResponse(data)
'''
