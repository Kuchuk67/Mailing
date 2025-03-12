from django.urls import path, reverse_lazy
from users.views import SignUpView, activate_user, ProfileUpdateView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("activate/", activate_user),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    # Востановление пароля
    path(
        "reset_password/",
        PasswordResetView.as_view(
            template_name="password_reset.html",
            success_url=reverse_lazy("users:password_reset_done"),
            email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        PasswordResetDoneView.as_view(
            template_name="password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html", success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
