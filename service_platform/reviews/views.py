from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from bookings.models import ServiceBooking
from .forms import ReviewForm

@login_required
def review_create(request, booking_id):
    booking = get_object_or_404(ServiceBooking, pk=booking_id, customer=request.user, status=ServiceBooking.COMPLETED)
    if hasattr(booking, "review"):
        messages.info(request, "Feedback is already submitted for this booking.")
        return redirect("customer_dashboard")
    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        review.customer = request.user
        review.provider = booking.provider
        review.save()
        messages.success(request, "Feedback submitted successfully.")
        return redirect("customer_dashboard")
    return render(request, "reviews/review_form.html", {"form": form, "booking": booking})
