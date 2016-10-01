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
from django.contrib.auth.models import User


def index(request):
    return render(request, 'quiz/index.html')


@login_required()
def quiz_batch_create(request):
    batch = QuizBatch.objects.create(user=request.user)
    return JsonResponse({u'status': u'ok', u'batch_id': batch.id})

@login_required()
def quiz_batch_characters(request, batch_id):
    if 'GET' != request.method:
        return JsonResponse({u'erro': 'request method err(only support GET method)'})
    if 'page_size' in request.GET:
        page_size = int(request.GET['page_size'])
    else:
        page_size = 30
    offset = random.randint(0, 237 ) #TODO
    character_statistics = CharacterStatistics.objects.filter(err_cnt__gte=50)[offset] #TODO
    char = character_statistics.char
    sql = u"select id, char, image, is_correct from segmentation_character where char='%s' \
    and (is_correct=1 or is_correct = -1) limit %d;" % (char,page_size)
    characters = Character.objects.raw(sql)
    char_lst = []
    for char in characters:
        obj = {
            u'id': char.id,
            u'char': char.char,
            u'image_url': char.image_url,
            u'is_correct': char.is_correct,
        }
        char_lst.append(obj)
    #char_lst_json = json.dumps(char_lst)
    return JsonResponse(char_lst, safe=False)


@login_required()
def set_correct(request, batch_id):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        character = Character.objects.get(pk=char_id)
        right_wrong = (character.is_correct == is_correct)
        quiz_result = QuizResult(user=request.user, character=character, is_correct=is_correct,
                                 right_wrong=right_wrong, batch_id=batch_id)
        quiz_result.save()
        data = {'status': 'ok'}
    elif 'charArr[]' in request.POST:
        round_number = request.session.get(batch_id+'round_number',1)
        request.session[batch_id+'round_number'] = round_number+1
        charArr = request.POST.getlist('charArr[]')
        quiz_result_lst = []
        is_correct = 1
        for char_id in charArr:
            character = Character.objects.get(pk=char_id)
            right_wrong = (character.is_correct == is_correct)
            quiz_result = QuizResult(user=request.user, character=character, is_correct=is_correct,
                                     right_wrong=right_wrong, batch_id=batch_id)
            quiz_result_lst.append(quiz_result)
        QuizResult.objects.bulk_create(quiz_result_lst)
        if round_number%4==0:
            #request.session['round_number'] = 1
            count = QuizResult.objects.filter(batch_id=batch_id).count()
            right_count = QuizResult.objects.filter(batch_id=batch_id, right_wrong=True).count()
            score = right_count * 1.0 / count
            try:
                batch = QuizBatch.objects.get(id=batch_id)
                batch.score = score
                batch.save()
                status = 'success' if score>0.85 else 'failure'
                if 'success' == status:
                    user = User.objects.get(username=request.user)
                    user.is_staff = True
                    user.save()
                data = {'status': status, 'score': score}
            except:
                data = {'status': 'error'}
        else:
            data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)