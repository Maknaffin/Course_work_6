# Generated by Django 4.2.1 on 2024-03-16 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, default='86982950', max_length=8, null=True, verbose_name='Код подтверждения почты'),
        ),
    ]