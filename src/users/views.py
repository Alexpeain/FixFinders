from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AdminUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')

class AdminRegisterView(CreateView):
    form_class = AdminUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admin Sign Up'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Role-based redirect
            if user.role == 'provider':
                # Redirect to completion if documents are missing
                from providers.models import ProviderProfile
                profile, _ = ProviderProfile.objects.get_or_create(user=user)
                if not profile.verification_photo_pink_card or not profile.verification_photo_smart_card:
                    messages.info(request, "Please complete your profile and upload verification documents.")
                    return redirect('providers:profile_complete')
                return redirect('providers:home')
            elif user.role == 'admin':
                return redirect('providers:admin_dashboard')
            return redirect('providers:home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('users:login')
