from django.core.exceptions import AppRegistryNotReady
from django.db.utils import IntegrityError

import logging
import math


class Generator:
    def generate(self):
        while True:
            try:
                from .models import Certificate
                break
            except AppRegistryNotReady:
                continue
        q = 1
        # добавляем "2" в БД, чтобы потом можно было с ее помощью генерировать недостающие простые числа
        Certificate.objects.get_or_create(N='2', a=2, q='1')
        cert_id = 1
        while True:
            R = 2
            while R < 4 * (q + 1):
                N = q * R + 1
                if 2 ** (N - 1) % N == 1 and 2 ** ((N - 1) / q) != 1:
                    try:
                        Certificate.objects.get_or_create(N=str(N), a=2, q=str(q))
                        logging.info(f'Added certificate ({N}, 2, {q})')
                    except IntegrityError:
                        pass
                elif self.brute_force_check(N):
                    logging.info(f'{N} is prime but was not certified by 2!')
                R += 2
            # получить следующее простое число из БД
            q = int(Certificate.objects.get(id=cert_id).N)
            cert_id += 1

    @staticmethod
    def brute_force_check(N: int) -> bool:
        for i in range(2, math.trunc(math.sqrt(N)) + 1):
            if N % i == 0:
                return False
        else:
            return True
