from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Mailing, MailingAttempt


def send_mailing_manual(mailing_id):
    """
    Отправляет рассылку и возвращает:
    - (True, "Успешно") если все письма отправлены.
    - (False, "Ошибка: {детали}") если были проблемы.
    """
    mailing = Mailing.objects.get(id=mailing_id)
    total_recipients = mailing.recipients.count()
    success_count = 0

    if mailing.status == "completed":
        return (False, "Рассылка уже завершена")

    if mailing.status == "created":
        mailing.status = "started"
        mailing.save()

    for recipient in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status="success",
                server_response="OK",
            )
            success_count += 1
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status="failed",
                server_response=str(e),
            )

    # Проверяем завершение
    if mailing.end_time <= timezone.now():
        mailing.status = "completed"
        mailing.save()

    if success_count == total_recipients:
        return (True, f"Все письма ({success_count}/{total_recipients}) отправлены")
    elif success_count > 0:
        return (False, f"Частично: {success_count}/{total_recipients} писем отправлено")
    else:
        return (False, "Все попытки завершились ошибкой")


