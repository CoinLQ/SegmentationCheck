# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from segmentation.models import Character, CharacterStatistics
from django.views import generic
import random
from django.db.models import F
import datetime
import json
from segmentation.models import CharacterStatistics
from .models import QuizResult, QuizBatch


def index(request):
    return render(request, 'quiz/index.html')


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


@login_required()
def quiz_batch_create(request):
    batch = QuizBatch.objects.create(user=request.user)
    return JsonResponse({u'status': u'ok', u'batch_id': batch.id})

@login_required()
def quiz_batch_characters(request, batch_id):
    offset = random.randint(0, 5) #TODO
    character_statistics = CharacterStatistics.objects.filter(err_cnt__gte=1)[offset] #TODO
    char = character_statistics.char
    sql = u"select id, char, image, is_correct from segmentation_character where char='%s' offset random() * 100 " \
          u"* (select count(*)/100 from segmentation_character where char='%s') limit 100;" \
          % (char, char)
    characters = Character.objects.raw(sql)
    char_lst = []
    for char in characters:
        obj = {
            u'id': char.id,
            u'char': char.char,
            u'image': char.image,
            u'is_correct': char.is_correct,
        }
        char_lst.append(obj)
    char_lst_json = json.dumps(char_lst)
    return JsonResponse({u'chars': char_lst_json}, safe=False)

@login_required()
def set_correct(request, batch_id):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        char = request.POST['char']
        character = Character.objects.get(pk=char_id)
        right_wrong = (character.is_correct == is_correct)
        quiz_result = QuizResult(user=request.user, character=character, is_correct=is_correct,
                                 right_wrong=right_wrong, batch_id=batch_id)
        quiz_result.save()
        data = {'status': 'ok'}
    elif 'charArr[]' in request.POST:
        check_char_number = request.session.get('check_char_number',0)
        request.session['check_char_number'] = check_char_number+1
        charArr = request.POST.getlist('charArr[]')
        char = request.POST['char']
        updateNum = int(request.POST['updateNum'])

        quiz_result_lst = []
        is_correct = 1
        char = request.POST['char']
        for char_id in charArr:
            character = Character.objects.get(pk=char_id)
            right_wrong = (character.is_correct == is_correct)
            quiz_result = QuizResult(user=request.user, character=character, is_correct=is_correct,
                                     right_wrong=right_wrong, batch_id=batch_id)
            quiz_result_lst.append(quiz_result)
        QuizResult.objects.bulk_create(quiz_result_lst)

        count = QuizResult.objects.filter(batch_id=batch_id).count()
        if count >= 400:
            right_count = QuizResult.objects.filter(batch_id=batch_id, right_wrong=True).count()
            score = right_count * 1.0 / count
            try:
                batch = QuizBatch.objects.get(id=batch_id)
                batch.score = score
                batch.save()
                data = {'status': 'ok', 'score': score}
            except:
                data = {'status': 'ok'}
        else:
            data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)