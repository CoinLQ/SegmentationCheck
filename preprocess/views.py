from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse
from catalogue.models import Tripitaka,Volume
from managerawdata.models import OPage
from catalogue.models import Tripitaka
from segmentation.models import Page
from django.views import generic
import json
import re
from django.conf import settings
from skimage import io

import cStringIO #for output memory file for save cut image
from django.core.files.storage import default_storage

class PreprocessIndex(generic.ListView):
    model = Tripitaka
    template_name = 'preprocess/preprocess.html'

#@login_required(login_url='/segmentation/login/')
def opage_cut(request):
    if request.method == 'POST':
        data = request.POST['data']
        d = json.loads(data)
        print d
        opage_id = d[0][u'opage_id']
        volume_id = d[0][u'volume_id']
        volume = get_object_or_404(Volume, pk=volume_id)
        volume_str = opage_id[0:opage_id.index('p')]
        opage = get_object_or_404(OPage, pk=opage_id)
        opage_image_path = opage.image.path
        opage_image = io.imread(opage_image_path, 0)
        for bar in d:
            bar_id = bar[u'bar_id']
            m = re.search('^p(\d+?)b(\d+?)',bar_id)
            if m:
                page_no = m.group(1)
                bar_no = m.group(2)
            page_id = '{0}p{1:05}b{2}'.format(volume_str,int(page_no),bar_no)
            top     = int(bar[u'top'])
            left    = int(bar[u'left'])
            width   = int(bar[u'width'])
            height  = int(bar[u'height'])
            page_image_name = page_id + u'.png'
            page_image_path = settings.PAGE_IMAGE_ROOT + page_image_name
            page_image = opage_image[top:top + height, left:left + width]
            memfile = cStringIO.StringIO()
            #io.imsave(memfile, page_image)
            #default_storage.save(page_image_path, memfile)
            io.imsave(page_image_path, page_image)
            page = Page(
                    id=page_id,
                    image=page_image_name,
                    width=width,
                    height=height,
                    o_page=opage,
                    volume = volume
                    )
            page.save()

        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

def text_process(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render_to_response('preprocess/text_process.html', {'page': page})


def preprocess_page(request):
    user = request.user
    return render_to_response('preprocess/preprocess_page.html', {'tripitaka_list': Tripitaka.objects.all(), 'user': user})
