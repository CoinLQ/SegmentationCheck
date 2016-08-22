from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from managerawdata.models import OPage
from django.views import generic

from rest_framework import viewsets
from .serializers import PreprocessSerializer


class PreprocessViewSet(viewsets.ModelViewSet):
    serializer_class = PreprocessSerializer
    queryset = OPage.objects.all()
    search_fields = ('pages_no', 'tripitaka')



class PreprocessIndex(generic.ListView):
    model = OPage
    template_name = 'preprocess/preprocess.html'

    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PreprocessIndex, self).dispatch(*args, **kwargs)


#@login_required(login_url='/segmentation/login/')
def bookpage_cut(request, bookpage_id):
    if request.method == 'POST':
        bookpage = get_object_or_404(OPage, pk=bookpage_id)
        data = request.POST['data']
        d = json.loads(data)
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

        return redirect('/segmentation/bookpages/%s/cut' % bookpage_id)
    else:
        opage = get_object_or_404(OPage, pk=bookpage_id).json_serialize()
        return JsonResponse({ u'opage':opage}, safe=False)
