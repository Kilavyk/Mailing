from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ContactsView, HomeView, ModerationView, ReportsView

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("moderation/", cache_page(60*5)(ModerationView.as_view()), name="moderation"),
    path("reports/", ReportsView.as_view(), name="reports"),
]
