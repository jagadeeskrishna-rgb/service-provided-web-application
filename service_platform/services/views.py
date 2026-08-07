from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ServiceCategoryForm
from .models import ServiceCategory


def admin_required(user):
    return user.is_authenticated and user.is_platform_admin


def category_list(request):
    query = request.GET.get("q", "")
    categories = ServiceCategory.objects.filter(is_active=True).annotate(provider_total=Count("providers", distinct=True))
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, "services/category_list.html", {"categories": categories, "query": query})


@login_required
@user_passes_test(admin_required)
def service_type_manage(request):
    query = request.GET.get("q", "")
    categories = ServiceCategory.objects.annotate(provider_total=Count("providers", distinct=True), booking_total=Count("bookings", distinct=True))
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, "services/service_type_manage.html", {"categories": categories, "query": query})


@login_required
@user_passes_test(admin_required)
def service_type_create(request):
    form = ServiceCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Service type added successfully.")
        return redirect("service_type_manage")
    return render(request, "services/service_type_form.html", {"form": form, "title": "Add Service Type"})


@login_required
@user_passes_test(admin_required)
def service_type_update(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    form = ServiceCategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Service type updated successfully.")
        return redirect("service_type_manage")
    return render(request, "services/service_type_form.html", {"form": form, "title": "Edit Service Type"})


@login_required
@user_passes_test(admin_required)
def service_type_delete(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    provider_count = category.providers.count()
    booking_count = category.bookings.count()
    if request.method == "POST":
        if provider_count or booking_count:
            category.is_active = False
            category.save(update_fields=["is_active"])
            messages.warning(request, "Service type has linked providers or bookings, so it was removed from the active customer list instead of deleting historical records.")
        else:
            category.delete()
            messages.success(request, "Service type deleted successfully.")
        return redirect("service_type_manage")
    return render(request, "services/service_type_confirm_delete.html", {"category": category, "provider_count": provider_count, "booking_count": booking_count})
