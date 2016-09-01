from django.shortcuts import render
from segmentation.models import Page, Character, CharacterStatistics
from django.core.serializers.json import DjangoJSONEncoder
from django.views import generic
import random
from django.db.models import F

class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CharacterLine):
            return {
                u'line_no': obj.line_no,
                u'left': obj.left,
                u'right': obj.right,
                u'char_lst': obj.char_lst,
            }
        if isinstance(obj, Character):
            return {
                u'id': obj.id,
                u'char': obj.char,
                u'line_no': obj.line_no,
                u'char_no': obj.char_no,
                u'top': obj.top,
                u'bottom': obj.bottom, u'is_correct': obj.is_correct, }
        return super(MyJsonEncoder, self).default(obj)

class CharacterLine:
    def __init__(self, line_no, left, right, char_lst):
        self.line_no = line_no
        self.left = left
        self.right = right
        self.char_lst = char_lst



class CharacterIndex(generic.ListView):
    template_name = 'task_checkchar/characters.html'

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
    mode = request.GET.get('mode')
    if mode == 'browse':  #browse mode  display all characters
        characters_list = Character.objects.filter(char=char).exclude(is_correct=-9)
        paginator = Paginator(characters_list, 30) # Show 30 characters per page
        page = request.GET.get('page')
        try:
            characters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            characters = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            characters = paginator.page(paginator.num_pages)
        charArr = json.dumps(characters,cls=charJsonEncoder)
        #totalPage = paginator.num_pages
        #currPage = characters.number
        items = paginator.count
        return JsonResponse({u'charArr':charArr, u'items':items,u'itemsOnPage':30,}, safe=False)
    else :        #check mode only display the unchecked characters (is_correct=0)
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

