from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse
from managerawdata.models import OPage
from segmentation.models import Page
from django.views import generic
import json


class PreprocessIndex(generic.ListView):
    model = OPage
    template_name = 'preprocess/preprocess.html'

#@login_required(login_url='/segmentation/login/')
def opage_cut(request, opage_id):
    if request.method == 'POST':
        opage = get_object_or_404(OPage, pk=opage_id)
        data = request.POST['data']
        d = json.loads(data)
        print d
#        bookpage_image_path = settings.BOOKPAGE_IMAGE_ROOT + bookpage.image
#        bookpage_image = io.imread(bookpage_image_path, 0)
#        for k, v in d.iteritems():
#            page_id = bookpage_id + '-' + k
#            top = v[u'top']
#            left = v[u'left']
#            width = v[u'width']
#            height = v[u'height']
#            page_image_name = page_id + u'.png'
#            page_image_path = settings.PAGE_IMAGE_ROOT + page_image_name
#            page_image = bookpage_image[top:top + height, left:left + width]
#            io.imsave(page_image_path, page_image)
#            page = Page(id=page_id, image=page_image_name, width=width, height=height, bookpage_id=bookpage_id)
#            page.save()

        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

def text_process(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render_to_response('preprocess/text_process.html', {'page': page})

