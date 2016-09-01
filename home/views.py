from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def demo(request):
    return render(request, 'home/demo.html')

def join_us(request):
    return render(request, 'home/join_us.html')
