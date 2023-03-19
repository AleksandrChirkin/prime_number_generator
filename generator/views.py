from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello, world!')


def health_check(request):
    return HttpResponse('Generator is alive and running!')
