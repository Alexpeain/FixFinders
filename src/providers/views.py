from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import ProviderProfile, Category
from .forms import ProviderProfileForm, ProviderUpdateForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class ProviderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'provider'

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProviderListView(ListView):
    template_name = 'providers/list.html'
    model = ProviderProfile
    context_object_name = 'providers'
    paginate_by = 20

    def get_queryset(self):
        # Only show verified providers in public list
        queryset = ProviderProfile.objects.filter(is_verified=True).select_related('category')
        category_slug = self.request.GET.get('category')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        town = self.request.GET.get('town')
        if town and town != "":
            queryset = queryset.filter(township=town)

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(business_name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(description__icontains=query)
            )
            
        return queryset.order_by('-is_verified', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.request.GET.get('category', '')
        context['current_town'] = self.request.GET.get('town', 'Muse')
        context['current_query'] = self.request.GET.get('q', '')
        return context

class ProviderDetailView(DetailView):
    template_name = 'providers/detail.html'
    model = ProviderProfile
    context_object_name = 'provider'

    def get_queryset(self):
        # Admins can see all, public can only see verified
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return ProviderProfile.objects.all()
        return ProviderProfile.objects.filter(is_verified=True)

# --- Verification Views ---

class ProfileCompletionView(LoginRequiredMixin, ProviderRequiredMixin, UpdateView):
    model = ProviderProfile
    form_class = ProviderProfileForm
    template_name = 'providers/profile_complete.html'
    
    def get_object(self, queryset=None):
        profile, created = ProviderProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        # Reset to pending on any update if not already approved
        if profile.verification_status != 'approved':
            profile.verification_status = 'pending'
            profile.is_verified = False
        profile.save()
        messages.success(self.request, "Profile updated successfully!")
        return redirect('providers:profile_edit')

class ProfileEditView(LoginRequiredMixin, ProviderRequiredMixin, UpdateView):
    model = ProviderProfile
    form_class = ProviderUpdateForm
    template_name = 'providers/profile_edit.html'
    success_url = reverse_lazy('providers:profile_edit')

    def get_object(self, queryset=None):
        return get_object_or_404(ProviderProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Public profile information updated.")
        return super().form_valid(form)

class AdminDashboardView(AdminRequiredMixin, ListView):
    model = ProviderProfile
    template_name = 'providers/admin_dashboard.html'
    context_object_name = 'providers'

    def get_queryset(self):
        status = self.request.GET.get('status', 'pending')
        return ProviderProfile.objects.filter(verification_status=status).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'pending')
        return context

def admin_verify_provider(request, pk):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        messages.error(request, "Permission denied.")
        return redirect('users:login')
    
    provider = get_object_or_404(ProviderProfile, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        reason = request.POST.get('rejection_reason', '')
        
        if action == 'approve':
            provider.verification_status = 'approved'
            provider.is_verified = True
            provider.rejection_reason = ""
            messages.success(request, f"Approved {provider.business_name}")
        elif action == 'reject':
            provider.verification_status = 'rejected'
            provider.is_verified = False
            provider.rejection_reason = reason
            messages.warning(request, f"Rejected {provider.business_name}")
        
        provider.save()
    return redirect('providers:admin_dashboard')