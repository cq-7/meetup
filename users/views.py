from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#登录
class SignInView(View):
    def get(self, request):
        return render(request, 'users/sign_in.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #注册了session
            login(request, user)
            messages.success(request, '登录成功')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, '用户名或者密码错误')
            return HttpResponseRedirect(reverse('users:sign_in'))

#注册
class SignUpView(View):
    def get(self, request):
        return render(request, 'users/sign_up.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        # 数据验证
        if password != password_confirmation:
            messages.error(request, '两次输入的密码不一致')
            return HttpResponseRedirect(reverse('users:sign_up'))

        # 注册用户
        User.objects.create_user(username, email, password)
        messages.success(request, '注册成功')
        return HttpResponseRedirect(reverse('users:sign_in'))

def sign_out(request):
    logout(request)
    messages.success(request, '你已经安全退出')
    return HttpResponseRedirect(reverse('index'))