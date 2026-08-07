from django.urls import path
from . import views

urlpatterns = [
    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("new/", views.booking_create, name="booking_create"),
    path("<int:pk>/", views.booking_detail, name="booking_detail"),
    path("<int:pk>/status/", views.booking_status_update, name="booking_status_update"),
    path("<int:pk>/cancel/", views.booking_cancel, name="booking_cancel"),
]
