# Generated by Django 3.2 on 2023-10-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_order_is_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='method',
            field=models.CharField(default='моно', max_length=10, verbose_name='Метод'),
        ),
        migrations.AddField(
            model_name='order',
            name='resolution',
            field=models.CharField(default='1 m/px', max_length=10, verbose_name='Разрешение'),
        ),
    ]
