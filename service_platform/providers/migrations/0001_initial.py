from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("services", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="ProviderProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("experience_years", models.PositiveIntegerField(default=0)),
                ("service_area", models.CharField(max_length=150)),
                ("bio", models.TextField(blank=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="providers", to="services.servicecategory")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="provider_profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["user__first_name", "user__username"]},
        )
    ]
