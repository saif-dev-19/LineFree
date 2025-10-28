from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserToken, Service, Organization
from .forms import TokenForm, RegisterForm, OrganizationForm, ServiceForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy



def is_admin(user):
    return user.is_staff


class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('home')





@login_required
def home(request):
    form = TokenForm()
    if request.method == "POST":
        form = TokenForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data["service_type"]
            org = form.cleaned_data["organization"]

            now_time = timezone.localtime().time()

            if service.start_time and service.end_time:
                if not (service.start_time <= now_time <= service.end_time):
                    messages.error(request, f"This service is only available from {service.start_time.strftime('%I:%M %p')} to {service.end_time.strftime('%I:%M %p')}.")
                    return redirect("home")

            # Token generate
            last_token = UserToken.objects.filter(service_type=service, organization=org).order_by("-token_number").first()
            new_number = last_token.token_number + 1 if last_token else 1
            token = form.save(commit=False)
            token.token_number = new_number
            token.user = request.user
            token.save()
            messages.success(request, f"Token generated successfully! Token #{new_number}")
            return redirect("my_token", token_id=token.id)
    organizations = Organization.objects.prefetch_related("services").all()
    user_tokens = UserToken.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "home.html", {"form": form, "user_tokens": user_tokens,'organizations': organizations})



@login_required
def my_token(request, token_id):
    token = get_object_or_404(UserToken, id=token_id)
    waiting_count = UserToken.objects.filter(
        service_type=token.service_type,
        organization=token.organization,
        status="Pending",
        created_at__lt=token.created_at
    ).count()
    return render(request, "my_token.html", {"token": token, "waiting_count": waiting_count})


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    tokens = UserToken.objects.all().order_by("created_at")
    return render(request, "admin_dashboard.html", {"tokens": tokens})


@login_required
@user_passes_test(is_admin)
def manage_organizations(request):
    organizations = Organization.objects.all()
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Organization '{form.cleaned_data['name']}' added successfully!")
            return redirect('manage_organizations')
    else:
        form = OrganizationForm()
    return render(request, 'manage_organizations.html', {'form': form, 'organizations': organizations})


@login_required
@user_passes_test(is_admin)
def update_status(request, token_id, status):
    token = get_object_or_404(UserToken, id=token_id)
    if token.status != "Completed":
        token.status = status
        token.save()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
def delete_token(request, token_id):
    token = get_object_or_404(UserToken, id=token_id)
    token.delete()
    return redirect('admin_dashboard')



def display_screen(request):
    now_serving = UserToken.objects.filter(status="Serving").order_by("created_at").first()
    return render(request, "display_screen.html", {"now_serving": now_serving})




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Role-based redirect after registration
            if user.is_staff:
                return redirect("admin_dashboard")
            else:
                return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@require_POST
def logout_page(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
@user_passes_test(is_admin)
def manage_services(request):
    services = Service.objects.select_related('organization').all()
    form = ServiceForm()

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Service '{form.cleaned_data['name']}' added successfully!")
            return redirect('manage_services')

    return render(request, 'manage_services.html', {'form': form, 'services': services})