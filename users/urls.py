from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (PasswordResetView, UserLoginView, UserLogoutView,
                    UserProfileView, UserRegisterView, email_verification)

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", cache_page(60*15)(UserProfileView.as_view()), name="profile"),
    path("verify/<str:token>/", email_verification, name="verification_email"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
