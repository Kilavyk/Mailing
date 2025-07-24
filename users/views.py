from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from .forms import UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class UserRegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = '/'


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
