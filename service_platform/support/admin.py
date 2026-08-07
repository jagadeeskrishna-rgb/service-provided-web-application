from django.contrib import admin

from .models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "booking", "subject", "status", "created_at", "resolved_by")
    list_filter = ("status", "created_at")
    search_fields = ("subject", "description", "customer__username", "admin_response")
