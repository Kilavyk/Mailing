from django.contrib import admin
from mailing.models import Recipient, Message, Mailing, MailingAttempt

admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)
