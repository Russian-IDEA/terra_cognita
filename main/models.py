from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    file = models.ImageField(upload_to='images/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField('Название', max_length=20)
    points = models.JSONField('Координаты')
    date = models.DateTimeField('Время исполнения')
    is_cancelled = models.BooleanField('Отменён', default=False)
    method = models.CharField('Метод', max_length=10, default='моно')
    resolution = models.CharField('Разрешение', max_length=10, default='1 m/px')
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class SatelliteModel(models.Model):
    s = models.CharField(max_length=100)
    t = models.CharField(max_length=100)
    view_angle = models.FloatField()

    def __str__(self):
        return str(self.id)
