from django.shortcuts import render, render_to_response
from django.template import RequestContext

def index(request):
    return render(request, 'home/index.html')

def demo(request):
    return render(request, 'home/demo.html')

def join_us(request):
    request.session['checkin_date'] = u'20150507'  # TODO
    return render(request, 'home/join_us.html')

def bad_request(request):
    response = render_to_response(
      '400.html',
      context_instance=RequestContext(request)
    )
    response.status_code = 400
    return response

def page_not_found(request):
    response = render_to_response(
      'error/404.html',
      context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response
  # return render_to_response('error/404.html', {'exception': ex},
  #                                     context_instance=RequestContext(request), status=404)