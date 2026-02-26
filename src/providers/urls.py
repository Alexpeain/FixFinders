from django.urls import path
from . import views  # <--- Import your views

app_name = 'providers'  # <--- Namespace (Important for {% url %} tags)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.ProviderListView.as_view(), name='list'),
    path('provider/<int:pk>/', views.ProviderDetailView.as_view(), name='detail'),
    
    # Verification & Profile
    path('profile/complete/', views.ProfileCompletionView.as_view(), name='profile_complete'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/verify/<int:pk>/', views.admin_verify_provider, name='admin_verify'),
]
