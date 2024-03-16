from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from service.forms import MessageForm, ClientForm, MailingOptionsForm
from service.models import MailingOptions, Message, Client, Logs


class BaseTemplateView(TemplateView):
    """Контроллер для вывода статистики на главной странице"""
    template_name = 'service/statistics.html'


class MessageListView(ListView):
    """Контроллер вывода списка сообщений"""
    model = Message


class MessageCreateView(CreateView):
    """Контроллер создания сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message_list')


class MessageUpdateView(UpdateView):
    """Контроллер редактирования сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message_list')


class MessageDeleteView(DeleteView):
    """Контроллер удаления сообщения"""
    model = Message
    success_url = reverse_lazy('service:message_list')


class ClientListView(ListView):
    """Контроллер вывода списка клиентов"""
    model = Client


class ClientCreateView(CreateView):
    """Контроллер создания клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client_list')


class ClientUpdateView(UpdateView):
    """Контроллер редактирования клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client_list')


class ClientDeleteView(DeleteView):
    """Контроллер удаления клиента"""
    model = Client
    success_url = reverse_lazy('service:client_list')


class MailingOptionsListView(ListView):
    """Контроллер создания рассылки"""
    model = MailingOptions


class MailingOptionsCreateView(CreateView):
    """Контроллер создания рассылки"""
    model = MailingOptions
    form_class = MailingOptionsForm
    success_url = reverse_lazy('service:mailing_list')


class MailingOptionsUpdateView(UpdateView):
    """Контроллер редактирования рассылки"""
    model = MailingOptions
    form_class = MailingOptionsForm
    success_url = reverse_lazy('service:mailing_update')


class MailingOptionsDeleteView(DeleteView):
    """Контроллер удаления рассылки"""
    model = MailingOptions
    success_url = reverse_lazy('service:mailing_delete')


class LogsListView(ListView):
    model = Logs
