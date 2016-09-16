from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

def index(request):
    return render(request, 'home/index.html')

def demo(request):
    return render(request, 'home/demo.html')

def join_us(request):
    return render(request, 'home/join_us.html')

@login_required
def app(request):
    context = {
        'permissions': json.dumps(list(request.user.get_all_permissions()))
    }

    template = 'home/app.html'
    return render(request, template, context)
