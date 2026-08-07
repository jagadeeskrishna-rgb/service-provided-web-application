from django.urls import path

from . import views

urlpatterns = [
    path("", views.customer_ticket_list, name="customer_ticket_list"),
    path("new/", views.ticket_create, name="ticket_create"),
]
