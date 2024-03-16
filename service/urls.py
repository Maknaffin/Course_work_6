from django.urls import path

from service.apps import ServiceConfig
from service.views import BaseTemplateView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MailingOptionsListView, \
    MailingOptionsCreateView, MailingOptionsUpdateView, MailingOptionsDeleteView, LogsListView

app_name = ServiceConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='main'),

    path('logs/', LogsListView.as_view(), name='logs'),

    path('mailings/', MailingOptionsListView.as_view(), name='mailing_list'),
    path('mailing_create/', MailingOptionsCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingOptionsUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingOptionsDeleteView.as_view(), name='mailing_delete'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
