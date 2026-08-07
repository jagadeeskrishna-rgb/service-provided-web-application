from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("booking", "customer", "provider", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("comment", "customer__username", "provider__username")
