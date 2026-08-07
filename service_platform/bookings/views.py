from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BookingForm, BookingStatusForm
from .models import ServiceBooking

@login_required
def customer_dashboard(request):
    bookings = ServiceBooking.objects.filter(customer=request.user).select_related("category", "provider")
    pending_review = bookings.filter(status=ServiceBooking.COMPLETED, review__isnull=True).first()
    if pending_review:
        messages.warning(request, "Please submit feedback for your completed booking before continuing.")
        return redirect("review_create", booking_id=pending_review.id)
    return render(request, "bookings/customer_dashboard.html", {"bookings": bookings})

@login_required
def booking_create(request):
    form = BookingForm(request.POST or None, initial={"service_address": request.user.address})
    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.customer = request.user
        booking.save()
        messages.success(request, "Booking request created successfully.")
        return redirect("customer_dashboard")
    return render(request, "bookings/booking_form.html", {"form": form})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(ServiceBooking.objects.select_related("category", "customer", "provider"), pk=pk)
    if not (request.user == booking.customer or request.user == booking.provider or request.user.is_platform_admin):
        messages.error(request, "You do not have permission to view this booking.")
        return redirect("role_redirect")
    return render(request, "bookings/booking_detail.html", {"booking": booking})

@login_required
def booking_status_update(request, pk):
    booking = get_object_or_404(ServiceBooking, pk=pk, provider=request.user)
    form = BookingStatusForm(request.POST or None, request.FILES or None, instance=booking)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Booking status updated.")
        return redirect("provider_dashboard")
    return render(request, "bookings/status_form.html", {"form": form, "booking": booking})

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(ServiceBooking, pk=pk)
    try:
        booking.cancel(request.user)
        messages.success(request, "Booking cancelled.")
    except ValidationError as exc:
        messages.error(request, exc.message)
    return redirect("customer_dashboard")
