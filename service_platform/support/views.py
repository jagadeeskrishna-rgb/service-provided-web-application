from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SupportTicketForm
from .models import SupportTicket


@login_required
def customer_ticket_list(request):
    if not request.user.is_customer:
        messages.error(request, "Only customers can access customer support tickets.")
        return redirect("role_redirect")
    tickets = SupportTicket.objects.filter(customer=request.user).select_related("booking")
    return render(request, "support/customer_ticket_list.html", {"tickets": tickets})


@login_required
def ticket_create(request):
    if not request.user.is_customer:
        messages.error(request, "Only customers can raise support tickets.")
        return redirect("role_redirect")
    form = SupportTicketForm(request.POST or None, customer=request.user)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.customer = request.user
        ticket.save()
        messages.success(request, "Support ticket raised successfully. Admin will review it.")
        return redirect("customer_ticket_list")
    return render(request, "support/ticket_form.html", {"form": form})
