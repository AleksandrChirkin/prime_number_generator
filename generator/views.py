from decimal import Decimal, getcontext, Overflow, ROUND_UP
from django.core.exceptions import AppRegistryNotReady
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from psutil import virtual_memory
from random import uniform
import math
import sys
# класс сертификата добавляется не сразу, а только после инициализации СУБД
while True:
    try:
        from .models import Certificate
        break
    except AppRegistryNotReady:
        continue
mem = virtual_memory()
generating = False


def index(request: WSGIRequest) -> HttpResponse:
    """Главная страница генератора"""
    global generating
    generating = False
    last_generated = Certificate.objects.order_by('-id')[0]
    largest_generated = Certificate.objects.order_by('-N')[0]
    certified_not_by_2 = Certificate.objects.filter(a__gt=2)
    context = {
        'last_generated': last_generated,
        'last_generated_cert': repr(last_generated),
        'largest_generated': largest_generated,
        'largest_generated_cert': repr(largest_generated),
        'certified_not_by_2': len(certified_not_by_2)
    }
    return render(request, "stats.html", context)


@csrf_exempt
def check(request: WSGIRequest) -> HttpResponse:
    """Проверить число на простоту"""
    if request.method == 'POST':
        N = request.POST['checked_num']
        if N == '2' or N == '3':
            return HttpResponse(f'{N} простое, но не сертифицируемое по теореме Диемитко!')
        try:
            return HttpResponse(f'{N} простое! Его сертификат: {repr(Certificate.objects.filter(N__exact=N)[0])}')
        except IndexError:  # если не нашлось сертификата
            return HttpResponse(
                f'Число {N} не является простым! (или сертификат простоты для него еще не был сгенерирован)')
    return HttpResponseNotAllowed('Только POST-метод разрешен для проведения проверки')


@csrf_exempt
def chain_generation(request: WSGIRequest) -> HttpResponse:
    """Быстрое получение больших простых чисел"""
    if request.method == 'POST':
        global mem, generating
        post_split = request.POST['root_num'].split('(')
        if len(post_split) == 1:
            root_num = int(post_split[0])
            try:
                Certificate.objects.filter(N__exact=root_num)[0]
            except IndexError:  # если не нашлось сертификата
                return HttpResponse(
                    f'Число {root_num} не является простым! (или сертификат простоты для него еще не был сгенерирован)')
        float_size = sys.getsizeof(float)
        getcontext().prec = float_size
        q = Decimal(post_split[0])
        two = Decimal(2)
        t = two * get_binary_len(q)
        generating = True
        try:
            while generating:
                getcontext().prec = float_size
                xi = Decimal(uniform(0, 1))
                getcontext().prec = int(get_int_part((t - 1) * Decimal(math.log10(2)))) + 1
                degree = two ** (t - 1)
                N = get_int_part(degree / q) + get_int_part((degree * xi) / q)
                if N % 2 == 1:
                    N += 1
                u = 0
                while generating:
                    p = (N + u) * q + 1  # кандидат в простые
                    # для вычисления степеней двойки выделяем половину от свободной ОП вычислительной машины
                    getcontext().prec = int(mem.available / 2)
                    if p > two ** t:
                        break
                    if two.__pow__(p - 1, p) == 1 and two.__pow__(N + u, p) != 1:
                        return HttpResponse(f'{p} ({get_binary_len(p)} бит)<br>')
                    u += 2
        except Overflow:
            return HttpResponse('Overflow')
    return HttpResponseNotAllowed('Только POST-метод разрешен для проведения проверки') if generating\
        else HttpResponse()


def get_binary_len(q: Decimal) -> int:
    getcontext().prec = len(str(q))
    result = ''
    while get_int_part(q) > 0:
        result = f'{q % 2}' + result
        q = get_int_part(q / 2)
    return len(result)


def get_int_part(original_decimal: Decimal) -> Decimal:
    return Decimal(str(original_decimal).split('.')[0])


def terminate_chain_generation(request: WSGIRequest) -> HttpResponse:
    global generating
    response_msg = 'Генерация прервана<br>' if generating else 'Прерывание не удалось, т.к. нет текущей генерации<br>'
    generating = False
    return HttpResponse(response_msg)


def certificates_list(request: WSGIRequest) -> HttpResponse:
    """Получить из базы данных список всех сертификатов и вернуть его в виде файла"""
    file_content = '\n'.join([repr(i) for i in Certificate.objects.order_by('N')])
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Length'] = len(file_content)
    response['Content-Disposition'] = 'attachment; filename=certificates.txt'
    return response
