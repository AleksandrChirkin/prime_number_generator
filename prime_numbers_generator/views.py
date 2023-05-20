from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect


def index(request: WSGIRequest) -> HttpResponseRedirect:
    """Перенаправление с главной страницы приложения на главную страницу генератора"""
    return HttpResponseRedirect('/generator/')
