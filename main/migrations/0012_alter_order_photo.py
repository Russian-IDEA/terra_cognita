# Generated by Django 3.2 on 2023-10-28 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20231028_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='photo',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.photo'),
        ),
    ]