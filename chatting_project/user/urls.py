from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.LoginView, name = 'login'),
    path("register/", views.SignupView, name = 'signup'),
    path("logout/", views.LogoutView, name = 'logout'),
    path("changepassword/", views.ChangePasswordView, name = 'change-password'),
    path("forgetpassword/", views.SendForgetEmail, name = 'forget-password'),
    path("change_password/<str:token>/", views.ChangeForgetPassword, name = 'change-forget-password'),
    path("verifyemail/", views.SendVerifyEmail, name = 'verify-email'),
    path("verifyemail/opt/", views.CheckOTP, name = 'otp-input')
]
