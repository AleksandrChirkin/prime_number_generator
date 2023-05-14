from django.core.exceptions import AppRegistryNotReady
from django.http import HttpResponse
while True:
    try:
        from .models import Certificate
        break
    except AppRegistryNotReady:
        continue


def index(request):
    all_certs = Certificate.objects.order_by('-id')
    last_generated = all_certs[0]
    ordered_certs = Certificate.objects.order_by('-N')
    largest_generated = ordered_certs[0]
    certified_not_by_2 = Certificate.objects.filter(a__gt=2)
    return HttpResponse(f'<!DOCTYPE html>\n'
                        f'<html lang="ru-RU">\n'
                        f'<head>\n'
                        f'<title>Статистика генератора</title>\n'
                        f'<meta charset="utf-8">\n'
                        f'</head>\n'
                        f'<body>\n'
                        f'<b>Сертификатов сгенерировано:</b> {last_generated.id}<br>\n'
                        f'<b>Последнее сертифицированное число:</b> {last_generated.N} <i>(его сертификат: {repr(last_generated)})</i><br>\n'
                        f'<b>Наибольшее сертифицированное число:</b> {largest_generated.N} <i>(его сертификат: {repr(largest_generated)}))</i><br>\n'
                        f'<b>Количество чисел, сертифицированных не двойкой:</b> {len(certified_not_by_2)}\n'
                        f'<form action="/generator/find">\n'
                        f'<button>Получить все сертификаты (может занять большое время)</button>'
                        f'</form>\n'
                        f'</body>\n'
                        f'</html>')

def get_all(request):
    file_content = '\n'.join([repr(i) for i in Certificate.objects.all()])
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Length'] = len(file_content)
    response['Content-Disposition'] = 'attachment; filename=certificates.txt'
    return response
