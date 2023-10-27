# Generated by Django 3.2 on 2023-10-27 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20231027_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s', models.CharField(max_length=100)),
                ('t', models.CharField(max_length=100)),
                ('view_angle', models.FloatField()),
            ],
        ),
    ]