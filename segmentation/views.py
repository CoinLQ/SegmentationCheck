from operator import attrgetter
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import QueryDict
from django.db.models.query import QuerySet
from django.core.paginator import Page as paginatorPageType

from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

from .models import Page, Character, CharacterStatistics

from django.views import generic

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,F
import json

from skimage import io
from page_processing import process_page,Char

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connection,transaction
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files import File
import cStringIO #for output memory file for save cut image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


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
                u'bottom': obj.bottom,
                u'is_correct': obj.is_correct,
            }
        return super(MyJsonEncoder, self).default(obj)

class charJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet) or isinstance(obj, paginatorPageType):
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

# Create your views here.
def index(request):
    return render(request, 'segmentation/index.html')

# use to demo UI compoent
def demo(request):
    return render(request, 'segmentation/demo.html')

#TODO  offline batch segment
@login_required(login_url='/segmentation/login/')
def run_batchsegment(request,number):
    data = {'status': 'pause service now'}
    return JsonResponse(data) #
    if not number:
        number =1
    pages = Page.objects.filter(is_correct=-9)[:number]
    for page in pages:
        print 'page.id: ', page.id.encode('utf-8')
        image_name = page.image.path
        text = page.text
        image = io.imread(image_name, 0)
        total_char_lst = process_page(image, text, page.id)
        character_lst = []
        temp_lst = []
        line_lst = []
        cur_line_no = 0
        for ch in total_char_lst:
            character = Character(id=ch.char_id.strip(), page_id=page.id, char=ch.char,
                                  image='',
                                  left=ch.left, right=ch.right,
                                  top=ch.top, bottom=ch.bottom,
                                  line_no=ch.line_no, char_no=ch.char_no,
                                  is_correct=-9)
            print Character
            character.save()
        page.is_correct = 0
        page.save()
    data = {'status': 'ok'}
    return JsonResponse(data)



#@login_required(login_url='/segmentation/login/')
def page_detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    text_line_lst = []
    for line in page.text.split(u'\n'):
        pos = line.find(u';')
        line=line[pos+1:]
        text_line_lst.append(line.lstrip())
    image_url = page.image.url

    characters = Character.objects.filter(page_id=page.id).order_by('line_no')
    temp_lst = []
    line_lst = []
    cur_line_no = 0
    for character in characters:
        character.width = character.right - character.left
        character.height = character.bottom - character.top
        if character.line_no != cur_line_no:
            if temp_lst:
                line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
                line_lst.append(line)
            cur_line_no = character.line_no
            temp_lst = [character]
        else:
            temp_lst.append(character)
    if temp_lst:
        line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
        line_lst.append(line)


    json_line_lst = json.dumps(line_lst,cls=MyJsonEncoder)
    return JsonResponse({ u'line_lst': json_line_lst, u'image_url':image_url, u'text': text_line_lst}, safe=False)
    #return render(request, 'segmentation/page_detail.html', {'page': page, 'line_lst': line_lst, 'text': text_line_lst})


class PageCheckView(generic.ListView):
    template_name = 'segmentation/page_check.html'
    def get_queryset(self):
        pk = self.kwargs['pk']
        #only show the page had been segment(right field is not equal 0),and had not been check
        return Page.objects.filter(id__startswith=pk).exclude(right=0).filter(is_correct=0)[:9]

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageCheckView, self).dispatch(*args, **kwargs)

#@login_required(login_url='/segmentation/login/')
def set_page_correct(request):
    if 'id' in request.POST:
        page_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        page = Page.objects.get(id = page_id)
        page.is_correct = is_correct
        page.save()
        data = {'status': 'ok'}
#        if is_correct == 1:
##TODO cut the char image
#            pageimg_file = page.image.path
#            page_image = io.imread(pageimg_file, 0)
#
#            char_lst = Character.objects.filter(page_id=page_id)
#            for ch in char_lst:
#                #TODO crop field outside the page_image can throug out: ValueError... tile cannot extend outside image
#                char_image = page_image[ch.top:ch.bottom, ch.left:ch.right]
#                memfile = cStringIO.StringIO()
#                io.imsave(memfile, char_image)
##save char image file
#                charimg_file = 'character_images/'+ch.page_id+"/"+ch.id+'.png'
#                default_storage.save(charimg_file, memfile)
#                ch.image = charimg_file #if the field has not been set,then uncomment this line
##update char is_correct state
#                ch.is_correct = 0 # is_correct set to 0 then the char will be show
#                ch.save()
##update the CharacterStatistics
#            cursor = connection.cursor()
#            raw_sql = '''
#            INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
#            SELECT
#                char,
#                count(segmentation_character."char") as total_cnt,
#                count(segmentation_character."char") as uncheck_cnt,
#                0,
#                0
#            FROM
#              public.segmentation_character where page_id='%s'
#              group by char
#            ON CONFLICT (char)
#            DO UPDATE SET
#            total_cnt=public.segmentation_characterstatistics.total_cnt + EXCLUDED.total_cnt,
#            uncheck_cnt=public.segmentation_characterstatistics.uncheck_cnt + EXCLUDED.uncheck_cnt,
#            err_cnt=public.segmentation_characterstatistics.err_cnt + EXCLUDED.err_cnt;
#            '''%(page_id)
#            print raw_sql
#            cursor.execute(raw_sql)
#                data = {'status': 'ok'}
#    elif 'pageArr[]' in request.POST:
#        pageArr = request.POST.getlist('pageArr[]')
#        Page.objects.filter(id__in = pageArr ).filter(is_correct=0).update(is_correct=1)
#        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

#TODO reSegment

def runSegment(request,page_id):
    page = Page.objects.get(id=page_id)
    image_name = page.image.url
    print image_name
    text = page.text
    image = io.imread(image_name, 0)
    total_char_lst = process_page(image, text, page_id)
    character_lst = []
    temp_lst = []
    line_lst = []
    cur_line_no = 0
    for ch in total_char_lst:
        character = Character(id=ch.char_id.strip(), page_id=page_id, char=ch.char,
                              image=ch.char_id.strip() + u'.jpg',
                              left=ch.left, right=ch.right,
                              top=ch.top, bottom=ch.bottom,
                              line_no=ch.line_no, char_no=ch.char_no,
                              is_correct=False)
        character.width = character.right - character.left
        character.height = character.bottom - character.top
        if character.line_no != cur_line_no:
            if temp_lst:
                line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
                line_lst.append(line)
            cur_line_no = character.line_no
            temp_lst = [character]
        else:
            temp_lst.append(character)
    if temp_lst:
        line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
        line_lst.append(line)

    json_line_lst = json.dumps(line_lst,cls=MyJsonEncoder)

    return JsonResponse({ u'line_lst': json_line_lst}, safe=False)


def cut_char_img( page_id,page_image,char_id):
    data = {'status': 'pause service now'}
    return JsonResponse(data)
    ch = Character.objects.get(id=char_id)
    charimg_file = 'character_images/'+page_id+"/"+char_id+'.png'
    char_image = page_image[ch.top:ch.bottom, ch.left:ch.right]
    memfile = cStringIO.StringIO()
    io.imsave(memfile, char_image)
#    contents = memfile.getvalue()
    default_storage.save(charimg_file, memfile)
    data = {'status': 'ok'}
    return JsonResponse(data)

#@login_required(login_url='/segmentation/login/')
def page_modify(request, page_id):
    data = {'status': 'pause service now'}
    return JsonResponse(data)
    data = {}
    if request.method == 'POST':
        for key, position in request.POST.iteritems():
            if u'-' in key:#adjust by chars
                pos = int(float(position))
                segs = key.split(u'-')
                if len(segs) == 3:
                    typ, line_no, char_no = segs
                    line_no = int(line_no)
                    char_no = int(char_no)
                    if char_no == 0:
                        char_id = page_id + u'%02dL%02d' % (line_no, 1)
                        Character.objects.filter(id=char_id).update(top=pos,is_correct=2)
                        cut_char_img(page_id,char_id)
                    else:
                        char_id = page_id + u'%02dL%02d' % (line_no, char_no)
                        Character.objects.filter(id=char_id).update(bottom=pos,is_correct=2)
                        #get page image
                        page = Page.objects.get(id = page_id)
                        pageimg_file = page.image.url
                        page_image = io.imread(pageimg_file, 0)

                        cut_char_img(page_id,page_image,char_id)

                        char_id = page_id + u'%02dL%02d' % (line_no, char_no + 1)
                        Character.objects.filter(id=char_id).update(top=pos,is_correct=2)
                        cut_char_img(page_id,page_image,char_id)
#                else: # adjust by colume
#                    typ, line_no = segs
#                    line_no = int(line_no)
#                    if line_no == 0:
#                        line_no = 1
#                        # update right
#                        Character.objects.filter(page_id=page_id, line_no=line_no).update(right=pos)
#                    else:
#                        # update left
#                        Character.objects.filter(page_id=page_id, line_no=line_no).update(left=pos)
#                        Character.objects.filter(page_id=page_id, line_no=line_no+1).update(right=pos)
#
        data = {'status': 'ok'}
    return JsonResponse(data)

def page_segmentation_line(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    characters = Character.objects.filter(page_id=page.id).order_by('line_no')
    temp_lst = []
    line_lst = []
    cur_line_no = 0
    for character in characters:
        character.width = character.right - character.left
        character.height = character.bottom - character.top
        if character.line_no != cur_line_no:
            if temp_lst:
                temp_lst.sort(key=attrgetter('char_no'))
                line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
                line_lst.append(line)
            cur_line_no = character.line_no
            temp_lst = [character]
        else:
            temp_lst.append(character)
    if temp_lst:
        temp_lst.sort(key=attrgetter('char_no'))
        line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
        line_lst.append(line)
    return JsonResponse(line_lst, safe=False, encoder=MyJsonEncoder)

class CharacterIndex(generic.ListView):
    template_name = 'segmentation/character_index.html'

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CharacterIndex, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return CharacterStatistics.objects.order_by('-uncheck_cnt')

class ErrPageIndex(generic.ListView):
    model = Character
    template_name = 'segmentation/err_page_index.html'

    def get_queryset(self):
        return Character.objects.filter(is_correct=-1).values('page').annotate(dcount=Count('page'))

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ErrPageIndex, self).dispatch(*args, **kwargs)


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
        characters = Character.objects.filter(char=char).filter(is_correct=0)[:30]
        qs = CharacterStatistics.objects.filter(char=char).values('uncheck_cnt')
        uncheck_cnt = qs[0]['uncheck_cnt']
        print uncheck_cnt
        charArr = json.dumps(characters,cls=charJsonEncoder)
        return JsonResponse({u'charArr':charArr, u'uncheck_cnt':uncheck_cnt,}, safe=False)



#@login_required(login_url='/segmentation/login/')
def set_correct(request):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        char = request.POST['char']
        if  Character.objects.filter(id=char_id).filter(is_correct=0).exists():
            CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=F('uncheck_cnt')-1)
        Character.objects.filter(id=char_id).update(is_correct=is_correct)
        CharacterStatistics.objects.filter(char=char).update(err_cnt=F('err_cnt')-is_correct)
        page_id = char_id[:14]
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
