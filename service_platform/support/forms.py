from django import forms

from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["booking", "subject", "description"]

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop("customer", None)
        super().__init__(*args, **kwargs)
        if customer is not None:
            self.fields["booking"].queryset = customer.customer_bookings.all()
        self.fields["booking"].required = False


class SupportTicketResolveForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["status", "admin_response"]
