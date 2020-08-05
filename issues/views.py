from django.shortcuts import get_object_or_404, render, redirect
from issues.models import Issue, Comment
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator


# 活动首页
def index(request):
    # return HttpResponse('Hello There~')
    issues = Issue.objects.order_by('-pub_at')
    paginator = Paginator(issues, 6)  # 实例化paginator，每页X条数据
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 根据当前页码获取实例对象

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
    page_num = request.GET.get('page', default='1')
    page_num = int(page_num)
    if page_num < 6:
        if paginator.num_pages <= 10:
            dis_range = range(1, paginator.num_pages + 1)
        else:
            dis_range = range(1, 11)
    elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
        dis_range = range(page_num - 5, page_num + 5)
    else:
        dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)

    return render(request, 'issues/index.html', {'page_obj': page_obj, 'dis_range ': dis_range})


# 新增活动
class AddView(View):
    def get(self, request):
        return render(request, 'issues/add.html')

    def post(self, request):
        if not request.user.is_authenticated:
            messages.success(request,'请登录后再操作')
            return HttpResponseRedirect(reverse('users:sign_in'))

        title = request.POST['title']
        content = request.POST['content']
        issue = Issue.objects.create(title=title, content=content, pub_at=timezone.now())
        messages.success(request, '新增成功')
        return HttpResponseRedirect(reverse('issues:detail', args=[issue.id]))


# 编辑活动
class ChangeView(View):
    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        return render(request, 'issues/change.html', {'issue': issue})

    def post(self, request, issue_id):
        title = request.POST['title']
        content = request.POST['content']
        Issue.objects.filter(id=issue_id).update(title=title, content=content)
        messages.success(request, '编辑成功')
        return HttpResponseRedirect(reverse('issues:detail', args=[issue_id]))


# 活动内页
class DetailView(View):
    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        return render(request, 'issues/detail.html', {'issue': issue})

    def post(self, request, issue_id):
        if not request.user.is_authenticated:
            messages.success(request,'请登录后再操作')
            return HttpResponseRedirect(reverse('users:sign_in'))



        content = request.POST['content']
        Comment.objects.create(content=content, issue_id=issue_id,
                               pub_at=timezone.now())

        issue = get_object_or_404(Issue, pk=issue_id)
        issue.comments_count = issue.comments_count + 1
        issue.save()

        messages.success(request, '新增成功')
        return HttpResponseRedirect(reverse('issues:detail', args=[issue_id]))


def delete(request, issue_id):
    #权限验证
    issue = get_object_or_404(Issue, pk=issue_id)
    if not request.user.is_authenticated and request.user.id != issue.user_id:
        messages.error(request, '您没有权限删除')
        return HttpResponseRedirect(reverse('issues:detail', args=[issue_id]))

    Issue.objects.filter(id=issue_id).delete()
    messages.success(request, '删除成功')
    return HttpResponseRedirect(reverse('issues:index'))
