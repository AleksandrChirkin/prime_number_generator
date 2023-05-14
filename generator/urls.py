from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('find', views.get_all, name='get_all')
]
