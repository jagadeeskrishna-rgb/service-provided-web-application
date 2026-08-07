from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CustomerRegistrationForm, ProviderRegistrationForm

def register_customer(request):
    form = CustomerRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "accounts/register.html", {"form": form, "title": "Customer Registration"})

def register_provider(request):
    form = ProviderRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "accounts/register.html", {"form": form, "title": "Provider Registration"})

@login_required
def role_redirect(request):
    user = request.user
    if user.is_platform_admin:
        return redirect("admin_dashboard")
    if user.is_provider:
        return redirect("provider_dashboard")
    return redirect("customer_dashboard")

LoginView = auth_views.LoginView
LogoutView = auth_views.LogoutView
