import smtplib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from service.models import Logs, MailingOptions
from datetime import datetime, timedelta


def send_and_log_mailer(obj: MailingOptions):
    for obj_email in obj.client_email.all():
        try:
            # Создание email для отправки
            email = EmailMultiAlternatives(
                subject=obj.mail_title.title,
                body=obj.mail_title.text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[obj_email.client_email],
            )
            now = datetime.now()
            now = timezone.make_aware(now, timezone.get_current_timezone())

            email.send()
            # Создание отчета по рассылке
            Logs.objects.create(
                send_name=obj.mail_title.title,
                last_try=now,
                status_try='Успешно',
                logs_owner=obj.options_owner,
                send_email=obj_email.client_email
            )
        except smtplib.SMTPException as e:
            Logs.objects.create(
                send_name=obj.mail_title.title,
                last_try=now,
                status_try='Ошибка',
                logs_owner=obj.options_owner,
                server_answer=e,
                send_email=obj_email.client_email
            )


def set_period():
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    next_try = now + timedelta(minutes=1)
    return next_try


def my_job():
    now = datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    mailing_list = MailingOptions.objects.all()
    for obj in mailing_list:
        if obj.is_active:
            if obj.mailing_status == 'Создана':
                if obj.mailing_start <= now:
                    obj.mailing_start = now
                    obj.mailing_status = 'Активна'
                    obj.save()
            if obj.mailing_status == 'Активна':
                if obj.mailing_finish <= now:
                    obj.mailing_status = 'Завершена'
                    obj.save()
                elif obj.mailing_start <= now:
                    send_and_log_mailer(obj)
                    if obj.mailing_period == 'Ежедневно':
                        obj.next_try += timedelta(days=1)
                        obj.save()
                    elif obj.mailing_period == 'Еженедельно':
                        obj.next_try += timedelta(days=7)
                        obj.save()
                    elif obj.mailing_period == 'Ежемесячно':
                        obj.next_try += timedelta(days=30)
                        obj.save()
