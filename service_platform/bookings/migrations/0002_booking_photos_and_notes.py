from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="servicebooking",
            name="provider_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="servicebooking",
            name="completion_photo",
            field=models.ImageField(blank=True, null=True, upload_to="booking_photos/completed/"),
        ),
        migrations.AddField(
            model_name="servicebooking",
            name="cancellation_photo",
            field=models.ImageField(blank=True, null=True, upload_to="booking_photos/cancelled/"),
        ),
    ]
