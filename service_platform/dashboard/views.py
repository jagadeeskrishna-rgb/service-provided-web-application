from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.models import User
from bookings.models import ServiceBooking
from providers.models import ProviderProfile
from reviews.models import Review
from services.models import ServiceCategory
from support.models import SupportTicket
from .forms import AdminBookingReassignForm, AdminSupportTicketResolveForm

def admin_required(user):
    return user.is_authenticated and user.is_platform_admin

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    context = {
        "customer_count": User.objects.filter(role=User.CUSTOMER).count(),
        "provider_count": ProviderProfile.objects.count(),
        "pending_provider_count": ProviderProfile.objects.filter(approval_status=ProviderProfile.PENDING).count(),
        "blocked_provider_count": ProviderProfile.objects.filter(approval_status=ProviderProfile.BLOCKED).count(),
        "category_count": ServiceCategory.objects.count(),
        "booking_count": ServiceBooking.objects.count(),
        "review_count": Review.objects.count(),
        "support_ticket_count": SupportTicket.objects.count(),
        "open_ticket_count": SupportTicket.objects.exclude(status=SupportTicket.RESOLVED).count(),
        "service_types": ServiceCategory.objects.annotate(provider_total=Count("providers", distinct=True))[:6],
        "recent_bookings": ServiceBooking.objects.select_related("customer", "provider", "category")[:10],
        "recent_tickets": SupportTicket.objects.select_related("customer", "booking")[:10],
        "status_counts": {status: ServiceBooking.objects.filter(status=status).count() for status, _ in ServiceBooking.STATUS_CHOICES},
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
@user_passes_test(admin_required)
def admin_customer_list(request):
    customers = User.objects.filter(role=User.CUSTOMER).prefetch_related("customer_bookings", "reviews_given", "support_tickets")
    return render(request, "dashboard/customer_list.html", {"customers": customers})


@login_required
@user_passes_test(admin_required)
def admin_provider_list(request):
    providers = ProviderProfile.objects.select_related("user").prefetch_related("categories")
    return render(request, "dashboard/provider_list.html", {"providers": providers})


@login_required
@user_passes_test(admin_required)
def provider_approve(request, pk):
    profile = get_object_or_404(ProviderProfile, pk=pk)
    profile.approve()
    messages.success(request, f"{profile.user.username} approved as a provider.")
    return redirect("admin_provider_list")


@login_required
@user_passes_test(admin_required)
def provider_block(request, pk):
    profile = get_object_or_404(ProviderProfile, pk=pk)
    profile.block("Blocked by admin from dashboard.")
    messages.warning(request, f"{profile.user.username} has been blocked.")
    return redirect("admin_provider_list")


@login_required
@user_passes_test(admin_required)
def admin_booking_list(request):
    bookings = ServiceBooking.objects.select_related("customer", "provider", "category").prefetch_related("support_tickets")
    return render(request, "dashboard/booking_list.html", {"bookings": bookings})


@login_required
@user_passes_test(admin_required)
def booking_reassign(request, pk):
    booking = get_object_or_404(ServiceBooking.objects.select_related("category", "provider"), pk=pk)
    form = AdminBookingReassignForm(request.POST or None, instance=booking)
    if request.method == "POST" and form.is_valid():
        try:
            booking.reassign(form.cleaned_data["provider"])
            messages.success(request, "Booking reassigned successfully.")
            return redirect("admin_booking_list")
        except ValidationError as exc:
            messages.error(request, exc.message)
    return render(request, "dashboard/booking_reassign.html", {"booking": booking, "form": form})


@login_required
@user_passes_test(admin_required)
def admin_review_list(request):
    reviews = Review.objects.select_related("booking", "customer", "provider")
    return render(request, "dashboard/review_list.html", {"reviews": reviews})


@login_required
@user_passes_test(admin_required)
def admin_ticket_list(request):
    tickets = SupportTicket.objects.select_related("customer", "booking", "resolved_by")
    return render(request, "dashboard/ticket_list.html", {"tickets": tickets})


@login_required
@user_passes_test(admin_required)
def ticket_resolve(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    form = AdminSupportTicketResolveForm(request.POST or None, instance=ticket)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        if ticket.status == SupportTicket.RESOLVED:
            ticket.resolved_by = request.user
            ticket.resolved_at = timezone.now()
        ticket.save()
        messages.success(request, "Support ticket updated successfully.")
        return redirect("admin_ticket_list")
    return render(request, "dashboard/ticket_resolve.html", {"ticket": ticket, "form": form})
