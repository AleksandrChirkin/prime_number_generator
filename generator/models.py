from django.db import models

# теорема Диемитко:
# N - нечетное, N = qR+1 > 1, q - простое, R - четное, R < 4(q+1); пусть существует такой a, что a^(n-1) % N == 1,
# a^((n-1)/q) % N != 1, тогда N - простое. (N, a, q) - сертификат простоты


class Certificate(models.Model):
    N = models.CharField(max_length=100, unique=True)
    a = models.PositiveIntegerField()
    q = models.CharField(max_length=100)

    def __str__(self):
        return f'\n{self.id}. ({self.N}, {self.a}, {self.q})'
