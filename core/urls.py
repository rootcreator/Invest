from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import (
    dashboard, deposit_page, invest_page, withdraw_page,
    HomePageView, CustomLoginView, register, csrf_token_view,
    password_reset_request
)

urlpatterns = [
    # API
    path("api/csrf-token/", csrf_token_view, name="csrf_token"),

    # Auth & Registration
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),  # Logout Redirects via settings.py
    path("register/", register, name="register"),

    # Main Pages
    path("", HomePageView.as_view(), name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("deposit/", deposit_page, name="deposit"),
    path("invest/", invest_page, name="invest"),
    path("withdraw/", withdraw_page, name="withdraw"),

    # Password Reset URLs
    path("password_reset/", password_reset_request, name="password_reset"),
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),
]
