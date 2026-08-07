from django import forms
from django.core.exceptions import ValidationError
from providers.models import ProviderProfile
from .models import ServiceBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ["category", "preferred_date", "preferred_time", "service_address", "problem_description"]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}),
        }

class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ["status", "provider_notes", "completion_photo", "cancellation_photo"]

    def clean_status(self):
        new_status = self.cleaned_data["status"]
        current_status = self.instance.status
        allowed = {
            ServiceBooking.ACCEPTED: {ServiceBooking.IN_PROGRESS, ServiceBooking.CANCELLED},
            ServiceBooking.IN_PROGRESS: {ServiceBooking.COMPLETED},
        }
        if new_status == current_status:
            return new_status
        if new_status not in allowed.get(current_status, set()):
            raise ValidationError("Invalid status change for the booking workflow.")
        return new_status


class BookingReassignForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ["provider"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.category_id:
            self.fields["provider"].queryset = self.fields["provider"].queryset.filter(
                role="provider",
                provider_profile__approval_status=ProviderProfile.APPROVED,
                provider_profile__is_available=True,
                provider_profile__categories=self.instance.category,
            ).distinct()
