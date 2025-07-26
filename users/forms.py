from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import CustomUser


class BaseFormStyle:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class UserRegisterForm(BaseFormStyle, UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'username'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=""
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=""
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user


class UserLoginForm(BaseFormStyle, AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )


class UserProfileForm(BaseFormStyle, UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'country', 'avatar')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Файл слишком большой (макс. 2MB)")
            if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Неподдерживаемый формат файла")
        return avatar


class UserDeleteForm(BaseFormStyle, forms.Form):
    confirm = forms.BooleanField(
        label="Я подтверждаю удаление аккаунта",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
