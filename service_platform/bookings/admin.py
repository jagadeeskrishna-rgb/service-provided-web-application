from django.contrib import admin
from .models import ServiceBooking

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "provider", "category", "preferred_date", "status", "created_at")
    list_filter = ("status", "category", "preferred_date")
    search_fields = ("customer__username", "provider__username", "service_address", "problem_description")
    readonly_fields = ("completion_photo", "cancellation_photo", "created_at", "updated_at")
