from django.contrib import admin
from django.urls import include, path

from . import views

# список всех групп URL-ов приложения
urlpatterns = [
    path('', views.index, name=''),
    path('generator/', include('generator.urls')),
    path('admin/', admin.site.urls)
]
