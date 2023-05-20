from django.db import models

# теорема Диемитко:
# N - нечетное, N = qR+1 > 1, q - простое, R - четное, R < 4(q+1); пусть существует такой a, что a^(N-1) % N == 1,
# a^((N-1)/q) % N != 1, тогда N - простое. (N, a, q) - сертификат простоты


class Certificate(models.Model):
    """Модель сертификата простоты для хранения в базе данных"""
    N = models.PositiveBigIntegerField(unique=True)
    a = models.PositiveIntegerField()
    q = models.PositiveBigIntegerField()

    def __repr__(self) -> str:
        return f'({self.N}, {self.a}, {self.q})'
