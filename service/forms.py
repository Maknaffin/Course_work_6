from django import forms

from service.models import Message, Client, Logs, MailingOptions
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['mailing_period', 'mail_title', 'client_email']:
                field.widget.attrs['class'] = 'form-select'
            elif field_name == 'is_active':
                field.widget.attrs['class'] = 'form'
            else:
                field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('message_owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('client_owner',)


class MailingOptionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingOptions
        exclude = ('options_owner', 'next_try', 'mailing_status',)


class MailingOptionsManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingOptions
        fields = ('is_active',)


class UsersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)
