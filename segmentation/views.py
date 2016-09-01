# -*- coding:utf-8 -*-
from operator import attrgetter
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import QueryDict
from django.db.models.query import QuerySet
from django.core.paginator import Page as paginatorPageType

from django.utils.functional import Promise
from django.utils.encoding import force_text

from segmentation.models import Page, Character

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

from django.core.serializers.json import DjangoJSONEncoder

from catalogue.models import Tripitaka


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

class Index(generic.ListView):
    model = Tripitaka
    template_name = 'segmentation/index.html'


#@login_required(login_url='/segmentation/login/')
def page_detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    text_line_lst = []
    for line in page.text.split(u'\n'):
        pos = line.find(u';')
        line=line[pos+1:]
        text_line_lst.append(line.lstrip())
    #image_url = page.image.url
    image_url = page.image

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

class ErrPageIndex(generic.ListView):
    model = Character
    template_name = 'segmentation/err_page_index.html'

    def get_queryset(self):
        return Character.objects.filter(is_correct=-1).values('page').annotate(dcount=Count('page'))

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ErrPageIndex, self).dispatch(*args, **kwargs)


def runSegment(request,page_id):
    page = Page.objects.get(id=page_id)
    image_name = page.image.url
    #print image_name
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
