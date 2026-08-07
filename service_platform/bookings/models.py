from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from providers.models import ProviderProfile
from services.models import ServiceCategory

class ServiceBooking(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_bookings")
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="provider_bookings", null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="bookings")
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    service_address = models.TextField()
    problem_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, db_index=True)
    provider_notes = models.TextField(blank=True)
    completion_photo = models.ImageField(upload_to="booking_photos/completed/", blank=True, null=True)
    cancellation_photo = models.ImageField(upload_to="booking_photos/cancelled/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "preferred_date"])]

    def __str__(self):
        return f"{self.category.name} booking for {self.customer.username}"

    def clean(self):
        if self.provider and not self.provider.is_provider:
            raise ValidationError("Assigned provider must have the provider role.")
        if self.provider:
            profile = ProviderProfile.objects.filter(user=self.provider, approval_status=ProviderProfile.APPROVED).first()
            if not profile or not profile.categories.filter(pk=self.category_id).exists():
                raise ValidationError("Assigned provider must be approved and must offer this service type.")

    def accept(self, provider):
        if self.status != self.PENDING:
            raise ValidationError("Only pending bookings can be accepted.")
        if not provider.is_provider:
            raise ValidationError("Only service providers can accept bookings.")
        profile = ProviderProfile.objects.filter(user=provider, approval_status=ProviderProfile.APPROVED, is_available=True).first()
        if not profile or not profile.categories.filter(pk=self.category_id).exists():
            raise ValidationError("Provider must be approved and must offer this service type.")
        self.provider = provider
        self.status = self.ACCEPTED
        self.save(update_fields=["provider", "status", "updated_at"])

    def reassign(self, provider):
        if not provider.is_provider:
            raise ValidationError("Selected user must be a provider.")
        profile = ProviderProfile.objects.filter(user=provider, approval_status=ProviderProfile.APPROVED, is_available=True).first()
        if not profile or not profile.categories.filter(pk=self.category_id).exists():
            raise ValidationError("Provider must be approved, available, and must offer this booking service.")
        self.provider = provider
        if self.status == self.PENDING:
            self.status = self.ACCEPTED
        self.save(update_fields=["provider", "status", "updated_at"])

    def mark_in_progress(self):
        if self.status != self.ACCEPTED:
            raise ValidationError("Only accepted bookings can move to in progress.")
        self.status = self.IN_PROGRESS
        self.save(update_fields=["status", "updated_at"])

    def mark_completed(self):
        if self.status != self.IN_PROGRESS:
            raise ValidationError("Only in-progress bookings can be completed.")
        self.status = self.COMPLETED
        self.save(update_fields=["status", "updated_at"])

    def cancel(self, user):
        if self.status not in [self.PENDING, self.ACCEPTED]:
            raise ValidationError("Only pending or accepted bookings can be cancelled.")
        if user != self.customer and not user.is_platform_admin:
            raise ValidationError("Only the customer or admin can cancel this booking.")
        self.status = self.CANCELLED
        self.save(update_fields=["status", "updated_at"])
