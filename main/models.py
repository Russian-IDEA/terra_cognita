from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField('Название', max_length=20)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()
    date = models.DateTimeField('Время исполнения')
    is_cancelled = models.BooleanField('Отменён', default=False)

    def __str__(self):
        return self.name
