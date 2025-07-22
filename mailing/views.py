from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from mailing.services import send_mailing_manual
from mailing.models import Mailing


def start_mailing(request, mailing_id):
    if not request.user.is_authenticated:
        return redirect('login')

    mailing = get_object_or_404(Mailing, id=mailing_id, owner=request.user)

    if send_mailing_manual(mailing_id):
        messages.success(request, 'Рассылка успешно запущена!')
    else:
        messages.error(request, 'Ошибка при отправке рассылки.')

    return redirect('mailing_detail', mailing_id=mailing_id)
