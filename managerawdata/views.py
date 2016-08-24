from django.shortcuts import render
from django.http import  JsonResponse
from django.views import generic
from catalogue.models import Tripitaka

class OpageIndex(generic.ListView):
    model = Tripitaka
    template_name = 'managerawdata/index.html'

#def index(request):
#    return render(request, 'managerawdata/index.html')

def opage_upload(request):
    def handle_uploaded_file(f):
        pk = 'aatttt'
        #MEDIA_ROOT = '/data/share/dzj_characters/'
        destination_file = '/data/share/dzj_characters/opage_images/'+pk+'.jpg'
        destination = open(destination_file, 'wb')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        #Page.objects.filter(id=pk).update(is_correct=2)
    if request.method == 'POST':
        print request.POST['file_id']
        print request.POST['kvId']
        print request.FILES['file_data']
        #handle_uploaded_file(request.FILES['file_data'])
        data = {'status': 'ok'}
        return JsonResponse(data)


    data = {'status': 'ok'}
    return JsonResponse(data)
