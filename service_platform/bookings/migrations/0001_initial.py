from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("services", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="ServiceBooking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("preferred_date", models.DateField()),
                ("preferred_time", models.TimeField()),
                ("service_address", models.TextField()),
                ("problem_description", models.TextField()),
                ("status", models.CharField(choices=[("pending", "Pending"), ("accepted", "Accepted"), ("in_progress", "In Progress"), ("completed", "Completed"), ("cancelled", "Cancelled")], db_index=True, default="pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bookings", to="services.servicecategory")),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="customer_bookings", to=settings.AUTH_USER_MODEL)),
                ("provider", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="provider_bookings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["status", "preferred_date"], name="bookings_se_status_3e20d3_idx")]},
        )
    ]
