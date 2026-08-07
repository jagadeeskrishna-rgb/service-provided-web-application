from django import forms

from .models import ServiceCategory


class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ["name", "description", "base_price", "is_active"]
