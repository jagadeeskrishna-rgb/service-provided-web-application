from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("register/customer/", views.register_customer, name="register_customer"),
    path("register/provider/", views.register_provider, name="register_provider"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("redirect/", views.role_redirect, name="role_redirect"),
]
