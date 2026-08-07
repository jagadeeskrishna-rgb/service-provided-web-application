from django.conf import settings
from django.db import models
from services.models import ServiceCategory

class ProviderProfile(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    BLOCKED = "blocked"
    APPROVAL_CHOICES = (
        (PENDING, "Pending Approval"),
        (APPROVED, "Approved"),
        (BLOCKED, "Blocked"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="provider_profile")
    categories = models.ManyToManyField(ServiceCategory, related_name="providers")
    experience_years = models.PositiveIntegerField(default=0)
    service_area = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default=PENDING, db_index=True)
    admin_notes = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__first_name", "user__username"]

    def __str__(self):
        service_names = ", ".join(self.categories.values_list("name", flat=True)[:3]) or "No services selected"
        return f"{self.user.get_full_name() or self.user.username} - {service_names}"

    @property
    def is_approved(self):
        return self.approval_status == self.APPROVED and self.user.is_active

    def approve(self):
        self.approval_status = self.APPROVED
        self.is_verified = True
        self.is_available = True
        self.user.is_active = True
        self.user.save(update_fields=["is_active"])
        self.save(update_fields=["approval_status", "is_verified", "is_available", "updated_at"])

    def block(self, notes=""):
        self.approval_status = self.BLOCKED
        self.is_available = False
        if notes:
            self.admin_notes = notes
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        self.save(update_fields=["approval_status", "is_available", "admin_notes", "updated_at"])
