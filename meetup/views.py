from django.http import HttpResponse
from django.shortcuts import render
from issues.models import Issue


def index(request):
    """
    index视图
    :param request: 包含了请求信息的请求对象
    :return: 响应对象
    """
    # return HttpResponse('Hello There~')
    issues = Issue.objects.order_by('-pub_at')
    return render(request, 'index.html',{'issues':issues})

# 关于我们
def about(request):
    return render(request, 'about.html')

# 404
def page_not_found(request, exception):
    return render(request, 'shared/404.html')

