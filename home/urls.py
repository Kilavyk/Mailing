from django.urls import path

from .views import ContactsView, HomeView, ModerationView

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("moderation/", ModerationView.as_view(), name="moderation"),
]
