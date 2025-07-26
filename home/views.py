from django.views.generic import TemplateView
from mailing.models import Mailing, Recipient


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Статистика для главной страницы
        if self.request.user.is_authenticated:
            # Количество всех рассылок пользователя
            context['user_mailings'] = Mailing.objects.filter(
                owner=self.request.user
            ).count()

            # Количество со статусом 'started'
            context['active_mailings'] = Mailing.objects.filter(
                owner=self.request.user,
                status='started'
            ).count()

            # Количество уникальных получателей
            context['unique_recipients'] = Recipient.objects.filter(
                mailing__owner=self.request.user
            ).distinct().count()
        else:
            context['user_mailings'] = 0
            context['active_mailings'] = 0
            context['unique_recipients'] = 0

        return context


class ContactsView(TemplateView):
    template_name = 'home/contacts.html'