# Generated by Django 4.2.1 on 2024-03-16 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, default='49929352', max_length=8, null=True, verbose_name='Код подтверждения почты'),
        ),
    ]
