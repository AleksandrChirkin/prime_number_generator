from django.core.exceptions import AppRegistryNotReady
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal, getcontext, MAX_PREC, Overflow
# класс сертификата добавляется не сразу, а только после инициализации СУБД
while True:
    try:
        from .models import Certificate

        break
    except AppRegistryNotReady:
        continue


def index(request: WSGIRequest) -> HttpResponse:
    """Главная страница генератора"""
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
        getcontext().prec = MAX_PREC
        result = []
        root_num = request.POST['root_num']
        try:
            Certificate.objects.filter(N__exact=root_num)[0]
        except IndexError:  # если не нашлось сертификата
            return HttpResponse(
                f'Число {root_num} не является простым! (или сертификат простоты для него еще не был сгенерирован)')
        q = Decimal(root_num)
        try:
            while len(result) < 100:
                R = Decimal(2)
                while R < 4 * (q + 1):
                    N = q * R + 1
                    first_decree = N - 1
                    second_decree = int(first_decree / q)
                    if pow(2, first_decree, N) == 1 and (first_decree % second_decree == 0 or
                                                            pow(2, second_decree, N) != 1):
                        result.append(str(N))
                        q = N
                        break
                    R += 2
        except Overflow:
            pass
        return HttpResponse('<br>'.join(result))
    return HttpResponseNotAllowed('Только POST-метод разрешен для проведения проверки')


def certificates_list(request: WSGIRequest) -> HttpResponse:
    """Получить из базы данных список всех сертификатов и вернуть его в виде файла"""
    file_content = '\n'.join([repr(i) for i in Certificate.objects.order_by('N')])
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Length'] = len(file_content)
    response['Content-Disposition'] = 'attachment; filename=certificates.txt'
    return response
