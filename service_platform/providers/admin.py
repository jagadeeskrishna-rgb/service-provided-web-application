from django.contrib import admin
from .models import ProviderProfile

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "service_list", "service_area", "approval_status", "experience_years", "is_verified", "is_available")
    list_filter = ("approval_status", "categories", "is_verified", "is_available")
    search_fields = ("user__username", "service_area", "bio")
    filter_horizontal = ("categories",)

    def service_list(self, obj):
        return ", ".join(obj.categories.values_list("name", flat=True))
