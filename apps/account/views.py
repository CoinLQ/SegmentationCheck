# -*- coding:utf-8 -*-
from account.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import JsonResponse

@csrf_protect
def register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            errors = []

            registerForm = RegistrationForm(request.POST)
            if not registerForm.is_valid():
                errors.extend(registerForm.errors.values())
                return JsonResponse({'error': errors})

            if password1 != password2:
                errors.append("两次输入的密码不一致!")
                return JsonResponse({'error': errors})

            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                errors.append("用户名已存在")
                return JsonResponse({'error': errors})

            user = User()
            user.username = username
            user.set_password(password1)
            user.email = email
            user.save()
            # 登录前需要先验证
            newUser = authenticate(username=username, password=password1)
            if newUser is not None:
                login(request, newUser)  # g*******************
                return HttpResponseRedirect('/')
    except Exception, e:
        errors.append(str(e))
        return JsonResponse({'error': errors})
