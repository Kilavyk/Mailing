from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Mailing, Message, Recipient


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'recipients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Фильтруем сообщения и получателей по владельцу
        if user:
            self.fields['message'].queryset = Message.objects.filter(owner=user)
            self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Введите корректный email адрес")

        if hasattr(self, 'instance') and hasattr(self.instance, 'owner'):
            owner = self.instance.owner
        else:
            owner = self.user if hasattr(self, 'user') else None

        if owner and Recipient.objects.filter(email=email, owner=owner).exists():
            if not self.instance or self.instance.email != email:
                raise forms.ValidationError("Этот email уже добавлен в вашем списке получателей")

        return email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
