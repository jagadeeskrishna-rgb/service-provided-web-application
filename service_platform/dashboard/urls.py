from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("customers/", views.admin_customer_list, name="admin_customer_list"),
    path("providers/", views.admin_provider_list, name="admin_provider_list"),
    path("providers/<int:pk>/approve/", views.provider_approve, name="provider_approve"),
    path("providers/<int:pk>/block/", views.provider_block, name="provider_block"),
    path("bookings/", views.admin_booking_list, name="admin_booking_list"),
    path("bookings/<int:pk>/reassign/", views.booking_reassign, name="booking_reassign"),
    path("reviews/", views.admin_review_list, name="admin_review_list"),
    path("tickets/", views.admin_ticket_list, name="admin_ticket_list"),
    path("tickets/<int:pk>/resolve/", views.ticket_resolve, name="ticket_resolve"),
]
