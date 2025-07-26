from django.views.generic import TemplateView
from mailing.models import Mailing, Recipient
from users.models import CustomUser
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Статистика для главной страницы
        context['total_mailings'] = Mailing.objects.count()
        context['total_active_mailings'] = Mailing.objects.filter(status='started').count()

        # Количество уникальных получателей (используем distinct() и Count)
        context['total_unique_recipients'] = Recipient.objects.aggregate(
            count=Count('email', distinct=True)
        )['count']

        # Информация по авторизованному пользователю
        if self.request.user.is_authenticated:
            context['user_mailings'] = Mailing.objects.filter(
                owner=self.request.user
            ).count()
            context['user_active_mailings'] = Mailing.objects.filter(
                owner=self.request.user,
                status='started'
            ).count()
            context['user_unique_recipients'] = Recipient.objects.filter(
                mailing__owner=self.request.user
            ).distinct().count()

        return context


class ContactsView(TemplateView):
    template_name = 'home/contacts.html'


class ModerationView(UserPassesTestMixin, TemplateView):
    template_name = 'home/moderation.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['mailings'] = Mailing.objects.all()
        context['unique_recipients'] = Recipient.objects.values('email').distinct()
        return context

    def post(self, request, *args, **kwargs):
        if 'block_user' in request.POST:
            user_id = request.POST.get('block_user')
            user = CustomUser.objects.get(id=user_id)
            user.is_active = False
            user.save()
            messages.success(request, f'Пользователь {user.email} заблокирован')

        elif 'block_mailing' in request.POST:
            mailing_id = request.POST.get('block_mailing')
            mailing = Mailing.objects.get(id=mailing_id)
            mailing.status = 'completed'
            mailing.save()
            messages.success(request, f'Рассылка #{mailing.id} отключена')

        return redirect(reverse('home:moderation'))
