from django.core.exceptions import AppRegistryNotReady
from django.db.utils import IntegrityError, OperationalError

import math


class Generator:
    """Генератор сертификатов простоты"""
    def generate(self) -> None:
        """Генерация сертификатов простоты"""
        # класс сертификата добавляется не сразу, а только после инициализации СУБД
        while True:
            try:
                from .models import Certificate
                break
            except AppRegistryNotReady:
                continue
        recovered = False
        certs = Certificate.objects.order_by('-id')
        try:
            last_cert = certs[0] # получаем последний сертификат
            q = last_cert.q # восстанавливаем q и R
            R = int((last_cert.N - 1) / last_cert.q)
            cert_id = Certificate.objects.get(N=q).id # определяем id сертификата простоты для q, чтобы можно было
            # определить, какое следующее простое число брать в качестве q
            recovered = True # признак того, что приложение восстановилось в состояние на момент его последнего завершения
            # необходим для избежания повторных вычислений степеней двойки для всех R, начиная с 2
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
                if self.brute_force_check(N):  # проверяем грубой силой, что позволит быстро отклонить предположение о
                    # простоте для многих чисел
                    prime_num_id = 0
                    while True:  # перебираем все возможные значения a
                        prime_num = Certificate.objects.all()[prime_num_id]
                        if pow(prime_num.N, first_decree, N) == 1 and (first_decree % second_decree == 0 or
                                                                       pow(prime_num.N, second_decree, N) != 1):
                            # условие теоремы Диемитко выполнилось
                            while True:
                                try:
                                    Certificate.objects.get_or_create(N=N, a=prime_num.N, q=q)
                                    break
                                except OperationalError:  # транзакция провалилась, пытаемся сделать ее снова
                                    continue
                                except IntegrityError:  # нашли в БД уже существующий сертификат для этого числа
                                    break
                            break
                        prime_num_id += 1
                R += 2
            # получить следующее простое число из БД и приравнять к нему q
            cert_id += 1
            q = int(Certificate.objects.get(id=cert_id).N)

    @staticmethod
    def brute_force_check(N: int) -> bool:
        """Проверка "грубой силой" на простоту (от 2 до корня из переданного в параметре числа)"""
        for i in range(2, math.trunc(math.sqrt(N)) + 1):
            if N % i == 0:
                return False
        else:
            return True
