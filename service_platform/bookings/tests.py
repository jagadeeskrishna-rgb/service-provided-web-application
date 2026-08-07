from datetime import date, time
from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.models import User
from providers.models import ProviderProfile
from services.models import ServiceCategory
from support.models import SupportTicket
from .models import ServiceBooking

class BookingWorkflowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username="cust", password="pass12345", role=User.CUSTOMER)
        self.provider = User.objects.create_user(username="prov", password="pass12345", role=User.PROVIDER)
        self.category = ServiceCategory.objects.create(name="Plumbing", description="Leak repair", base_price=300)
        self.second_category = ServiceCategory.objects.create(name="AC Repair", description="AC service", base_price=700)
        self.profile = ProviderProfile.objects.create(user=self.provider, service_area="North Area", approval_status=ProviderProfile.APPROVED, is_verified=True)
        self.profile.categories.set([self.category, self.second_category])
        self.booking = ServiceBooking.objects.create(customer=self.customer, category=self.category, preferred_date=date.today(), preferred_time=time(9, 0), service_address="Main Road", problem_description="Tap repair")

    def test_provider_accepts_pending_booking(self):
        self.booking.accept(self.provider)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, ServiceBooking.ACCEPTED)
        self.assertEqual(self.booking.provider, self.provider)

    def test_non_provider_cannot_accept_booking(self):
        with self.assertRaises(ValidationError):
            self.booking.accept(self.customer)

    def test_customer_can_cancel_pending_booking(self):
        self.booking.cancel(self.customer)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, ServiceBooking.CANCELLED)

    def test_multiple_providers_can_share_same_service_category(self):
        second_provider = User.objects.create_user(username="prov2", password="pass12345", role=User.PROVIDER)
        second_profile = ProviderProfile.objects.create(user=second_provider, service_area="South Area", approval_status=ProviderProfile.APPROVED)
        second_profile.categories.set([self.category])
        self.assertEqual(ProviderProfile.objects.filter(categories=self.category).count(), 2)

    def test_pending_provider_cannot_accept_booking(self):
        pending_user = User.objects.create_user(username="pending", password="pass12345", role=User.PROVIDER)
        pending_profile = ProviderProfile.objects.create(user=pending_user, service_area="Pending Area", approval_status=ProviderProfile.PENDING)
        pending_profile.categories.set([self.category])
        with self.assertRaises(ValidationError):
            self.booking.accept(pending_user)

    def test_customer_can_raise_support_ticket(self):
        ticket = SupportTicket.objects.create(customer=self.customer, booking=self.booking, subject="Need help", description="Please help with this booking.")
        self.assertEqual(ticket.status, SupportTicket.OPEN)
