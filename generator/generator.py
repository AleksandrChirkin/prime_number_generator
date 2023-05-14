from django.core.exceptions import AppRegistryNotReady
from django.db.utils import IntegrityError, OperationalError

import math


class Generator:
    def generate(self):
        while True:
            try:
                from .models import Certificate
                break
            except AppRegistryNotReady:
                continue
        recovered = False
        certs = Certificate.objects.order_by('-id')
        try:
            last_cert = certs[0]
            q = last_cert.q
            R = int((last_cert.N - 1) / last_cert.q)
            cert_id = Certificate.objects.get(N=q).id
            recovered = True
        except IndexError:  # если в БД ничего нет
            # добавляем "2" в БД, чтобы потом можно было с ее помощью генерировать недостающие простые числа
            Certificate.objects.get_or_create(N=2, a=2, q=1)
            q = 1
            R = 2
            cert_id = 1
        while True:
            if recovered:
                recovered = False
            else:
                R = 2
            while R < 4 * (q + 1):
                N = q * R + 1
                first_decree = N - 1
                second_decree = int(first_decree / q)
                if self.brute_force_check(N):
                    prime_num_id = 0
                    while True:
                        prime_num = Certificate.objects.all()[prime_num_id]
                        if pow(prime_num.N, first_decree, N) == 1 and (first_decree % second_decree == 0 or
                                                                       pow(prime_num.N, second_decree, N) != 1):
                            while True:
                                try:
                                    Certificate.objects.get_or_create(N=N, a=prime_num.N, q=q)
                                    break
                                except OperationalError:
                                    continue
                                except IntegrityError:
                                    break
                            break
                        prime_num_id += 1
                R += 2
            # получить следующее простое число из БД
            cert_id += 1
            q = int(Certificate.objects.get(id=cert_id).N)

    @staticmethod
    def brute_force_check(N: int) -> bool:
        for i in range(2, math.trunc(math.sqrt(N)) + 1):
            if N % i == 0:
                return False
        else:
            return True
