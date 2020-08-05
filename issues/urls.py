from django.contrib import admin
from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:issue_id>/', views.DetailView.as_view(), name='detail'),
    path('add/', views.AddView.as_view(), name='add'),
    path('<int:issue_id>/change', views.ChangeView.as_view(), name='change'),
    path('<int:issue_id>/delete/', views.delete, name='delete'),
]