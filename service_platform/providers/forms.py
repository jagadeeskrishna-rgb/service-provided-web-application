from django import forms
from .models import ProviderProfile

class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ["categories", "experience_years", "service_area", "bio", "is_available"]
        widgets = {
            "categories": forms.CheckboxSelectMultiple,
        }
