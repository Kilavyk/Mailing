from django.urls import path

from .views import (MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingUpdateView, MessageCreateView,
                    RecipientCreateView, message_delete, recipient_delete,
                    start_mailing, MessageUpdateView, RecipientUpdateView)

app_name = "mailing"

urlpatterns = [
    path("", MailingListView.as_view(), name="list"),
    path("create/", MailingCreateView.as_view(), name="create"),
    path("<int:pk>/", MailingDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", MailingUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="delete"),
    path("<int:mailing_id>/start/", start_mailing, name="start"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/delete/", message_delete, name="message_delete"),
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/<int:pk>/delete/", recipient_delete, name="recipient_delete"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("recipient/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
]
