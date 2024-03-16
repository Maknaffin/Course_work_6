from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from service.forms import MessageForm, ClientForm, MailingOptionsForm, MailingOptionsManagerForm, UsersForm
from service.models import MailingOptions, Message, Client, Logs
from users.models import User


class BaseTemplateView(TemplateView):
    """Контроллер для вывода статистики на главной странице"""
    template_name = 'service/statistics.html'


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

    # def form_valid(self, form): # валидация с шадулером
    #     send_params = form.save()
    #     send_params.options_owner = self.request.user
    #     send_params.next_try = set_period()
    #     send_params.save()
    #
    #     return super().form_valid(form)


class MailingOptionsUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования рассылки"""
    model = MailingOptions
    form_class = MailingOptionsForm
    success_url = reverse_lazy('service:mailing_list')

    # def form_valid(self, form): # валидация с шадулером
    #     send_params = form.save()
    #     self.model.send_status = send_params.send_status
    #     send_params.next_try = set_period()
    #     send_params.save()
    #
    #     return super().form_valid(form)

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
    success_url = reverse_lazy('service:mailing_delete')


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
