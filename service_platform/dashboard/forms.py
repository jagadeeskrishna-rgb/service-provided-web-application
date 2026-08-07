from django import forms

from bookings.forms import BookingReassignForm
from support.forms import SupportTicketResolveForm


class AdminBookingReassignForm(BookingReassignForm):
    pass


class AdminSupportTicketResolveForm(SupportTicketResolveForm):
    pass
