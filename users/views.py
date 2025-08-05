import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import (PasswordResetForm, UserDeleteForm, UserLoginForm,
                    UserProfileForm, UserRegisterForm)
from .models import CustomUser


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home:home")

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка входа. Проверьте правильность email и пароля."
        )
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    url = reverse_lazy("home:home")

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Вы успешно вышли из системы")
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.verification_token = token  # Используем правильное поле
        user.save()

        # Отправляем HTML-письмо
        send_mail(
            subject="Подтверждение регистрации",
            message="",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=render_to_string(
                "users/verification_email.html",
                {
                    "user": user,
                    "domain": settings.DOMAIN,
                    "token": token,
                },
            ),
        )

        messages.success(
            self.request,
            "Регистрация прошла успешно! Пожалуйста, проверьте вашу почту для подтверждения email.",
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomUser, verification_token=token)
    user.is_active = True
    user.verification_token = None  # Очищаем токен после использования
    user.save()
    messages.success(
        request, "Ваш email успешно подтверждён! Теперь вы можете войти в систему."
    )
    return redirect(reverse("users:login"))  # Правильный URL для перенаправления


class UserProfileView(UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if "avatar" in self.request.FILES:
            self.object.avatar = self.request.FILES["avatar"]
        self.object.save()
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, FormView):
    template_name = "users/delete_account.html"
    form_class = UserDeleteForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = self.request.user
        logout(self.request)
        user.delete()
        messages.success(self.request, "Ваш аккаунт был успешно удален")
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "users/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower()
        try:
            user = CustomUser.objects.get(email=email)
            # Генерируем новый пароль
            new_password = secrets.token_urlsafe(16)
            user.password = make_password(new_password)
            user.save()

            # Отправляем письмо с новым паролем
            send_mail(
                subject="Восстановление пароля",
                message=f"Ваш новый пароль: {new_password}\n\nРекомендуем изменить его, но это не предусмотрено функционалом.\nНам очень жаль, честно-честно😔😔😔.",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            messages.success(self.request, "Новый пароль отправлен на ваш email.")
        except CustomUser.DoesNotExist:
            messages.error(self.request, "Пользователь с таким email не найден.")

        return super().form_valid(form)
