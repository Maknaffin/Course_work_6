# Generated by Django 4.2.1 on 2024-03-11 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingoptions',
            name='client_email',
            field=models.ManyToManyField(to='service.client', verbose_name='Контактный email'),
        ),
    ]