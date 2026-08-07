from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from bookings.models import ServiceBooking
from .forms import ProviderProfileForm
from .models import ProviderProfile

def provider_required(user):
    return user.is_authenticated and user.is_provider

@login_required
@user_passes_test(provider_required)
def provider_dashboard(request):
    profile = ProviderProfile.objects.filter(user=request.user).first()
    bookings = ServiceBooking.objects.filter(provider=request.user).select_related("category", "customer")
    if profile and profile.is_approved:
        pending = ServiceBooking.objects.filter(status=ServiceBooking.PENDING, category__in=profile.categories.all())
    else:
        pending = ServiceBooking.objects.none()
    return render(request, "providers/dashboard.html", {"profile": profile, "bookings": bookings, "pending": pending})

@login_required
@user_passes_test(provider_required)
def provider_profile(request):
    profile = ProviderProfile.objects.filter(user=request.user).first()
    form = ProviderProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        provider_profile = form.save(commit=False)
        provider_profile.user = request.user
        provider_profile.save()
        form.save_m2m()
        if provider_profile.approval_status == ProviderProfile.PENDING:
            messages.info(request, "Profile saved. Admin approval is required before you can accept jobs.")
        return redirect("provider_dashboard")
    return render(request, "providers/profile_form.html", {"form": form})

@login_required
@user_passes_test(provider_required)
def accept_booking(request, pk):
    booking = get_object_or_404(ServiceBooking, pk=pk, status=ServiceBooking.PENDING)
    try:
        booking.accept(request.user)
        messages.success(request, "Booking accepted successfully.")
    except ValidationError as exc:
        messages.error(request, exc.message)
    return redirect("provider_dashboard")
