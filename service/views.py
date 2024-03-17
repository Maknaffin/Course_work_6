import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from service.forms import MessageForm, ClientForm, MailingOptionsForm, MailingOptionsManagerForm, UsersForm
from service.models import MailingOptions, Message, Client, Logs
from service.services import set_period
from users.models import User


class BaseTemplateView(TemplateView):
    """Контроллер для вывода статистики и статей на главной странице"""
    template_name = 'service/statistics.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['full_list'] = MailingOptions.objects.all().count()
        context_data['active_list'] = MailingOptions.objects.filter(is_active=True).count()
        context_data['unique_clients_list'] = Client.objects.all().count()
        articles_count = Blog.objects.all().count()
        if settings.CACHE_ENABLED:
            key = f'random_articles'
            article_list = cache.get(key)
            if article_list is None:
                article_list = random.sample(list(Blog.objects.all()), articles_count)
                cache.set(key, article_list)
        else:
            article_list = random.sample(list(Blog.objects.all()), articles_count)
        context_data['random_articles'] = article_list

        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер вывода списка сообщений"""
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(message_owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message_list')

    def form_valid(self, form):
        message_params = form.save()
        message_params.message_owner = self.request.user
        message_params.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('service:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления сообщения"""
    model = Message
    success_url = reverse_lazy('service:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер вывода списка клиентов"""
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client_owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.client_owner = self.request.user
        send_params.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления клиента"""
    model = Client
    success_url = reverse_lazy('service:client_list')


class MailingOptionsListView(LoginRequiredMixin, ListView):
    """Контроллер создания рассылки"""
    model = MailingOptions

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager'):
            queryset = queryset.all()
        else:
            queryset = queryset.filter(options_owner=self.request.user)
        return queryset


class MailingOptionsCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания рассылки"""
    model = MailingOptions
    form_class = MailingOptionsForm
    success_url = reverse_lazy('service:mailing_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.options_owner = self.request.user
        send_params.next_try = set_period()
        send_params.save()

        return super().form_valid(form)


class MailingOptionsUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования рассылки"""
    model = MailingOptions
    form_class = MailingOptionsForm
    success_url = reverse_lazy('service:mailing_list')

    def form_valid(self, form):
        send_params = form.save()
        self.model.mailing_status = send_params.mailing_status
        send_params.next_try = set_period()
        send_params.save()

        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager'):
            return MailingOptionsManagerForm
        return MailingOptionsForm


class MailingOptionsDeleteView(DeleteView):
    """Контроллер удаления рассылки"""
    model = MailingOptions
    success_url = reverse_lazy('service:mailing_list')


class LogsListView(LoginRequiredMixin, ListView):
    """Контлоллер для вывода списка отчета по рассылкам"""
    model = Logs

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(logs_owner=self.request.user)
        return queryset


class UsersListView(LoginRequiredMixin, ListView):
    """Контлоллер для вывода списка пользователей"""
    model = User
    template_name = 'service/users_table.html'


class UsersUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsersForm
    template_name = 'service/user_activity_form.html'
    success_url = reverse_lazy('service:users_table')
