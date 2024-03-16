from django.contrib import admin

from service.models import Message, MailingOptions, Client


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')


@admin.register(MailingOptions)
class MailingOptionsAdmin(admin.ModelAdmin):
    list_display = ('mailing_name', 'mailing_start', 'mailing_finish', 'mailing_status', 'is_active')


@admin.register(Client)
class ClientHistoryAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'comment')
