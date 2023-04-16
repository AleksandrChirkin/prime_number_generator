from django.core.exceptions import AppRegistryNotReady
from django.db.utils import IntegrityError
from pathlib import Path

import logging
import math
import signal


class Generator:
    def __init__(self):
        self.backup = 'backup_params.txt'
        self.q = 1
        self.R = 2
        signal.signal(signal.SIGINT, self.write_backup)

    def generate(self):
        while True:
            try:
                from .models import Certificate
                break
            except AppRegistryNotReady:
                continue
        recovered = False
        if Path(self.backup).exists():
            with open(self.backup) as backup_file:
                backup_content = backup_file.read().split(',')
            self.q = int(backup_content[0])
            self.R = int(backup_content[1])
            cert_id = Certificate.objects.get(N=self.q).id
            recovered = True
        else:
            # добавляем "2" в БД, чтобы потом можно было с ее помощью генерировать недостающие простые числа
            Certificate.objects.get_or_create(N='2', a=2, q='1')
            cert_id = 1
        while True:
            if recovered:
                recovered = False
            else:
                self.R = 2
            while self.R < 4 * (self.q + 1):
                N = self.q * self.R + 1
                first_decree = N - 1
                second_decree = int(first_decree / self.q)
                if pow(2, first_decree, N) == 1 and (first_decree % second_decree == 0 or
                                                     pow(2, second_decree, N) != 1):
                    try:
                        Certificate.objects.get_or_create(N=N, a=2, q=self.q)
                        logging.info(f'({N}, 2, {self.q})')
                    except IntegrityError:
                        pass
                elif self.brute_force_check(N):
                    logging.info(f'{N} is prime but was not certified by 2!')
                self.R += 2
            # получить следующее простое число из БД
            self.q = int(Certificate.objects.get(id=cert_id).N)
            cert_id += 1

    def write_backup(self, signum, frame):
        with open(self.backup, mode='w') as backup_params:
            backup_params.write(f'{self.q},{self.R}')
        exit()

    @staticmethod
    def brute_force_check(N: int) -> bool:
        for i in range(2, math.trunc(math.sqrt(N)) + 1):
            if N % i == 0:
                return False
        else:
            return True
