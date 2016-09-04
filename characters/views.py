from django.shortcuts import render
from django.http import  JsonResponse
from segmentation.models import Page, Character, CharacterStatistics
from django.core.serializers.json import DjangoJSONEncoder
from django.views import generic
import random
from django.db.models import F
from django.core.paginator import Page as paginatorPageType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

class charJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, paginatorPageType):
            arr = []
            for ch in obj:
                arr.append({
                u'id': ch.id,
                u'image': '/character_images/'+ch.page_id+'/'+ch.image,
                u'is_correct': ch.is_correct,
                            })
            return arr
        return super(charJsonEncoder, self).default(obj)


class CharacterLine:
    def __init__(self, line_no, left, right, char_lst):
        self.line_no = line_no
        self.left = left
        self.right = right
        self.char_lst = char_lst

class CharacterIndex(generic.ListView):
    model =  CharacterStatistics
    template_name = 'characters/character_index.html'


class Task(generic.ListView):
    template_name = 'characters/characters.html'

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CharacterIndex, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return CharacterStatistics.objects.order_by('-uncheck_cnt')

    def sample(self):
        with open('static/alternative_char_list.txt') as f:
            txt = f.read()
            char_list = txt.split(',')
        char = random.choice(char_list).strip()
        return CharacterStatistics.objects.filter(char=char)

#@login_required(login_url='/segmentation/login/')
def character_check(request, char):
    if not char:
        with open('static/alternative_char_list.txt') as f:
            txt = f.read()
            char_list = txt.split(',')
        char = random.choice(char_list).strip()
    characters = Character.objects.filter(char=char).filter(is_correct=0)[:30]
    qs = CharacterStatistics.objects.filter(char=char).values('uncheck_cnt','total_cnt')
    total_cnt = qs[0]['total_cnt']
    uncheck_cnt = qs[0]['uncheck_cnt']
    charArr = json.dumps(characters,cls=charJsonEncoder)
    return JsonResponse({u'charArr':charArr, u'total_cnt':total_cnt,u'uncheck_cnt':uncheck_cnt,u'char':char}, safe=False)



#@login_required(login_url='/segmentation/login/')
def set_correct(request):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        char = request.POST['char']
        char.encode('utf-8')
        if  Character.objects.filter(id=char_id).filter(is_correct=0).exists():
            CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=F('uncheck_cnt')-1)
        Character.objects.filter(id=char_id).update(is_correct=is_correct)
        CharacterStatistics.objects.filter(char=char).update(err_cnt=F('err_cnt')-is_correct)
        data = {'status': 'ok'}
    elif 'charArr[]' in request.POST:
        charArr = request.POST.getlist('charArr[]')
        char = request.POST['char']
        updateNum = int(request.POST['updateNum'])
        Character.objects.filter(id__in = charArr ).filter(is_correct=0).update(is_correct=1)
        CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=F('uncheck_cnt')-updateNum)
        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

#from tasks import update_char_stastics
#
#def test(request):
#    update_char_stastics.delay()
#    data = {'status': 'ok'}
#    return JsonResponse(data)
