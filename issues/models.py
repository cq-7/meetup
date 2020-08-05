from django.db import models
from django.contrib.auth.models import User

# 定义活动
class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户',default=1)  # 外键
    title = models.CharField(max_length=20, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    pub_at = models.DateTimeField(verbose_name='发布时间')
    comments_count = models.IntegerField(default=0, verbose_name='评论数')
    class Meta:
        verbose_name = '活动'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.title

# 评论
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户',default=1)  # 外键
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, verbose_name='活动',default=1)  # 外键
    email = models.CharField(max_length=20,verbose_name='邮箱')
    content = models.TextField(verbose_name='内容')
    pub_at = models.DateTimeField(verbose_name='发布时间')

    class Meta:
        verbose_name = '评论'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.username
