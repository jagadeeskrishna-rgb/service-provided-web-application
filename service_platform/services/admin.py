from django.contrib import admin
from .models import ServiceCategory

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "base_price", "is_active", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
