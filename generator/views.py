from django.core.exceptions import AppRegistryNotReady
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
while True:
    try:
        from .models import Certificate
        break
    except AppRegistryNotReady:
        continue


def index(request):
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


def check(request):
    if request.method == 'POST':
        try:
            N = request.POST['checked_num']
            return HttpResponse(repr(Certificate.objects.filter(N__exact=N)[0]))
        except IndexError:
            return HttpResponse(f'{N} не является простым! (или еще не было сгенерировано)')
    return HttpResponseNotAllowed('Only POST method is allowed for check')


def list(request):
    file_content = '\n'.join([repr(i) for i in Certificate.objects.order_by('N')])
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Length'] = len(file_content)
    response['Content-Disposition'] = 'attachment; filename=certificates.txt'
    return response
