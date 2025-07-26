from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Mailing, Recipient, Message
from .forms import MailingForm, MessageForm, RecipientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Сообщение успешно создано")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages_list'] = Message.objects.filter(owner=self.request.user)
        return context

class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Получатель успешно добавлен")
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients_list'] = Recipient.objects.filter(owner=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@require_POST
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk, owner=request.user)
    message.delete()
    messages.success(request, "Сообщение успешно удалено")
    return redirect('mailing:message_create')


@require_POST
def recipient_delete(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk, owner=request.user)
    recipient.delete()
    messages.success(request, "Получатель успешно удален")
    return redirect('mailing:recipient_create')


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