# Generated by Django 3.2 on 2023-10-27 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(verbose_name='Время исполнения'),
        ),
    ]
