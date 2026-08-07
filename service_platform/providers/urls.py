from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.provider_dashboard, name="provider_dashboard"),
    path("profile/", views.provider_profile, name="provider_profile"),
    path("bookings/<int:pk>/accept/", views.accept_booking, name="accept_booking"),
]
