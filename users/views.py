from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from .forms import UserDeleteForm, UserLoginForm, UserProfileForm, UserRegisterForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home:home')



class UserLogoutView(LogoutView):
    url = reverse_lazy('home:home')


    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Вы успешно вышли из системы')
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request,"Регистрация прошла успешно! Теперь вы можете войти в систему.")
        return super().form_valid(form)


class UserProfileView(UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'avatar' in self.request.FILES:
            self.object.avatar = self.request.FILES['avatar']
        self.object.save()
        return super().form_valid(form)

class DeleteAccountView(LoginRequiredMixin, FormView):
    template_name = 'users/delete_account.html'
    form_class = UserDeleteForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = self.request.user
        logout(self.request)
        user.delete()
        messages.success(self.request, 'Ваш аккаунт был успешно удален')
        return super().form_valid(form)























#
# from django.views.generic import CreateView, UpdateView
# from django.contrib.auth.views import LoginView, LogoutView
# from .models import CustomUser
# from .forms import UserRegisterForm, UserProfileForm
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.contrib.auth import logout
#
#
# class UserLoginView(LoginView):
#     template_name = 'users/login.html'
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('home:home')
#
#     def form_valid(self, form):
#         """Вызывается при успешной авторизации"""
#         response = super().form_valid(form)
#         return response
#
#     def form_invalid(self, form):
#         messages.error(
#             self.request,
#             "Ошибка входа. Проверьте правильность email и пароля."
#         )
#         return super().form_invalid(form)
#
#
# class UserLogoutView(LogoutView):
#     url = reverse_lazy('home:home')
#
#     def dispatch(self, request, *args, **kwargs):
#         logout(request)
#         messages.info(request, 'Вы успешно вышли из системы')
#         return super().dispatch(request, *args, **kwargs)
#
#
# class UserRegisterView(CreateView):
#     model = CustomUser
#     form_class = UserRegisterForm
#     template_name = 'users/register.html'
#     success_url = reverse_lazy('users:login')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request,"Регистрация прошла успешно! Теперь вы можете войти в систему.")
#         return response
#
#
# class UserProfileView(UpdateView):
#     model = CustomUser
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'
#     success_url = reverse_lazy('users:profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         if 'avatar' in self.request.FILES:
#             self.object.avatar = self.request.FILES['avatar']
#         self.object.save()
#         return super().form_valid(form)
