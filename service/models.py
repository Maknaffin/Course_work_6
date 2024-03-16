from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}

mailing_period_CHOICES = (
    ('Ежедневно', 'Ежедневно'),
    ('Еженедельно', 'Еженедельно'),
    ('Ежемесячно', 'Ежемесячно')
)

mailing_status_CHOICES = (
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
    ('Завершена', 'Завершена')
)


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма', unique=True)
    text = models.TextField(verbose_name='Тело письма')
    message_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                                      on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class MailingOptions(models.Model):
    mailing_name = models.CharField(max_length=200, verbose_name='Наименование рассылки', default=None)
    mailing_start = models.DateTimeField(verbose_name='Время начала рассылки', default=None)
    mailing_finish = models.DateTimeField(verbose_name='Время окончания рассылки', default=None)
    next_try = models.DateTimeField(verbose_name='Следующая попытка', **NULLABLE)
    mailing_period = models.CharField(max_length=20, verbose_name='Периодичность', choices=mailing_period_CHOICES,
                                      default='')
    mail_title = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Тема рассылки',
                                   default=None)
    mailing_status = models.CharField(max_length=20, verbose_name='Статус рассылки', choices=mailing_status_CHOICES,
                                      default='Создана')
    client_email = models.ManyToManyField('Client', verbose_name="Контактный email")
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    options_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                                      on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.mailing_name}"

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'


class Client(models.Model):
    client_email = models.CharField(max_length=150, verbose_name="Контактный email", unique=True)
    client_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                                     on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.client_name} - {self.client_email}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Logs(models.Model):
    last_try = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата и время последней попытки')
    status_try = models.CharField(max_length=20, verbose_name='Статус попытки')
    server_answer = models.TextField(verbose_name='Ответ сервера', default='', **NULLABLE)
    send_name = models.CharField(max_length=200, verbose_name='Наименование рассылки', default=None)
    send_email = models.EmailField(max_length=150, verbose_name='Почта отправки', **NULLABLE)
    logs_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь',
                                   on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.status_try}: {self.last_try}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
