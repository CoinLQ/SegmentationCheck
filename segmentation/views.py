from operator import attrgetter
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Page, Character

class CharacterLine:
    def __init__(self, line_no, left, right, char_lst):
        self.line_no = line_no
        self.left = left
        self.right = right
        self.char_lst = char_lst

# Create your views here.
def index(request):
    return render(request, 'segmentation/index.html')

def page_detail(request, page_id):
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
                line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
                line_lst.append(line)
            cur_line_no = character.line_no
            temp_lst = [character]
        else:
            temp_lst.append(character)
    if temp_lst:
        line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
        line_lst.append(line)
    return render(request, 'segmentation/page_detail.html',
                  {'page': page, 'line_lst': line_lst})

def page_modify(request, page_id):
    data = {}
    if request.method == 'POST':
        for key, position in request.POST.iteritems():
            if u'-' in key:
                pos = int(float(position))
                segs = key.split(u'-')
                if len(segs) == 3:
                    typ, line_no, char_no = segs
                    line_no = int(line_no)
                    char_no = int(char_no)
                    if char_no == 0:
                        char_id = page_id + u'%02dL%02d' % (line_no, 1)
                        Character.objects.filter(id=char_id).update(top=pos)
                    else:
                        char_id = page_id + u'%02dL%02d' % (line_no, char_no)
                        Character.objects.filter(id=char_id).update(bottom=pos)
                        char_id = page_id + u'%02dL%02d' % (line_no, char_no + 1)
                        Character.objects.filter(id=char_id).update(top=pos)
                else:
                    typ, line_no = segs
                    line_no = int(line_no)
                    if line_no == 0:
                        line_no = 1
                        # update right
                        Character.objects.filter(page_id=page_id, line_no=line_no).update(right=pos)
                    else:
                        # update left
                        Character.objects.filter(page_id=page_id, line_no=line_no).update(left=pos)
                        Character.objects.filter(page_id=page_id, line_no=line_no+1).update(right=pos)

        data = {'status': 'ok'}
    return JsonResponse(data)

def character_check(request, char):
    print char
    characters = Character.objects.filter(char=char)
    return render(request, 'segmentation/character_check.html', {'char': char, 'characters': characters})

def set_correct(request):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        Character.objects.filter(id=char_id).update(is_correct=is_correct)
    data = {'status': 'ok'}
    return JsonResponse(data)

def page_image(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, 'segmentation/page_detail.html',
                  {'page': page})
