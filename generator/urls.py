from django.urls import path

from . import views

# список URL-ов для генератора
urlpatterns = [
    path('', views.index, name='index'),
    path('check', views.check, name='check'),
    path('list', views.certificates_list, name='list')
]
