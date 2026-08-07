from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CUSTOMER = "customer"
    PROVIDER = "provider"
    ADMIN = "admin"
    ROLE_CHOICES = (
        (CUSTOMER, "Customer"),
        (PROVIDER, "Service Provider"),
        (ADMIN, "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    @property
    def is_customer(self):
        return self.role == self.CUSTOMER

    @property
    def is_provider(self):
        return self.role == self.PROVIDER

    @property
    def is_platform_admin(self):
        return self.is_staff or self.role == self.ADMIN
