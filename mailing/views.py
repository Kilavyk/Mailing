from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Mailing, Recipient, Message
from .forms import MailingForm


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'

    def get_success_url(self):
        return reverse_lazy('mailing:detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


# Функция для запуска рассылки
def start_mailing(request, mailing_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    mailing = get_object_or_404(Mailing, id=mailing_id, owner=request.user)

    # Импортируем функцию отправки
    from .services import send_mailing_manual

    success, message = send_mailing_manual(mailing_id)

    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('mailing:detail', pk=mailing_id)