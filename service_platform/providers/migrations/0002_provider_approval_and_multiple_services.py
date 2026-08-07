from django.db import migrations, models


def copy_existing_category(apps, schema_editor):
    ProviderProfile = apps.get_model("providers", "ProviderProfile")
    for profile in ProviderProfile.objects.exclude(category_id=None):
        profile.categories.add(profile.category_id)


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0001_initial"),
        ("services", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="providerprofile",
            name="categories",
            field=models.ManyToManyField(related_name="providers", to="services.servicecategory"),
        ),
        migrations.AddField(
            model_name="providerprofile",
            name="approval_status",
            field=models.CharField(choices=[("pending", "Pending Approval"), ("approved", "Approved"), ("blocked", "Blocked")], db_index=True, default="pending", max_length=20),
        ),
        migrations.AddField(
            model_name="providerprofile",
            name="admin_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="providerprofile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RunPython(copy_existing_category, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="providerprofile",
            name="category",
        ),
    ]
