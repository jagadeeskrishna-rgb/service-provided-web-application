from datetime import date, time
from django.core.management.base import BaseCommand
from accounts.models import User
from bookings.models import ServiceBooking
from providers.models import ProviderProfile
from services.models import ServiceCategory
from support.models import SupportTicket

class Command(BaseCommand):
    help = "Create demo categories, users, providers, and bookings."

    def handle(self, *args, **options):
        categories = [
            ("Plumbing", "Pipe leakage, tap repair, bathroom fittings", 350),
            ("Electrical", "Switch, wiring, fan, and lighting work", 400),
            ("Cleaning", "Home, kitchen, bathroom, and deep cleaning", 600),
            ("Painting", "Wall painting and small paint repair work", 800),
            ("AC Repair", "AC servicing, cooling issue diagnosis, and minor repair", 700),
            ("Appliance Repair", "Washing machine, fridge, and appliance service", 500),
            ("General Labour", "Loading, shifting, and general household labour", 450),
        ]
        category_objects = {}
        for name, description, price in categories:
            category_objects[name], _ = ServiceCategory.objects.get_or_create(name=name, defaults={"description": description, "base_price": price})

        admin, _ = User.objects.get_or_create(username="admin", defaults={"role": User.ADMIN, "is_staff": True, "is_superuser": True, "email": "admin@example.com"})
        admin.set_password("admin12345")
        admin.save()
        customer, _ = User.objects.get_or_create(username="customer", defaults={"role": User.CUSTOMER, "email": "customer@example.com", "phone": "9999999999", "address": "Demo Street, Local Area"})
        customer.set_password("customer123")
        customer.save()
        provider, _ = User.objects.get_or_create(username="provider", defaults={"role": User.PROVIDER, "email": "provider@example.com", "phone": "8888888888", "address": "Provider Colony"})
        provider.set_password("provider123")
        provider.save()
        ac_provider_one, _ = User.objects.get_or_create(username="ac_mechanic_one", defaults={"role": User.PROVIDER, "email": "ac1@example.com", "phone": "7777777771", "address": "North Service Area"})
        ac_provider_one.set_password("provider123")
        ac_provider_one.save()
        ac_provider_two, _ = User.objects.get_or_create(username="ac_mechanic_two", defaults={"role": User.PROVIDER, "email": "ac2@example.com", "phone": "7777777772", "address": "South Service Area"})
        ac_provider_two.set_password("provider123")
        ac_provider_two.save()
        pending_provider, _ = User.objects.get_or_create(username="pending_provider", defaults={"role": User.PROVIDER, "email": "pending@example.com", "phone": "7777777773", "address": "Pending Area"})
        pending_provider.set_password("provider123")
        pending_provider.save()

        plumber_profile, _ = ProviderProfile.objects.get_or_create(user=provider, defaults={"experience_years": 4, "service_area": "Local Area", "bio": "Experienced local plumber and appliance helper.", "approval_status": ProviderProfile.APPROVED, "is_verified": True})
        plumber_profile.categories.set([category_objects["Plumbing"], category_objects["Appliance Repair"]])
        ac_profile_one, _ = ProviderProfile.objects.get_or_create(user=ac_provider_one, defaults={"experience_years": 5, "service_area": "North Service Area", "bio": "AC mechanic for servicing and cooling issues.", "approval_status": ProviderProfile.APPROVED, "is_verified": True})
        ac_profile_one.categories.set([category_objects["AC Repair"], category_objects["Appliance Repair"]])
        ac_profile_two, _ = ProviderProfile.objects.get_or_create(user=ac_provider_two, defaults={"experience_years": 3, "service_area": "South Service Area", "bio": "AC mechanic for installation and minor repair.", "approval_status": ProviderProfile.APPROVED, "is_verified": True})
        ac_profile_two.categories.set([category_objects["AC Repair"], category_objects["Electrical"]])
        pending_profile, _ = ProviderProfile.objects.get_or_create(user=pending_provider, defaults={"experience_years": 1, "service_area": "Pending Area", "bio": "New provider awaiting approval.", "approval_status": ProviderProfile.PENDING})
        pending_profile.categories.set([category_objects["Cleaning"]])

        booking, _ = ServiceBooking.objects.get_or_create(customer=customer, category=category_objects["Plumbing"], preferred_date=date.today(), preferred_time=time(10, 30), service_address=customer.address, problem_description="Kitchen sink leakage")
        SupportTicket.objects.get_or_create(customer=customer, booking=booking, subject="Need update on booking", defaults={"description": "Customer wants admin help for booking progress."})
        self.stdout.write(self.style.SUCCESS("Demo data created."))
