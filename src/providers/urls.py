from django.urls import path
from . import views  # <--- Import your views

app_name = 'providers'  # <--- Namespace (Important for {% url %} tags)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.ProviderListView.as_view(), name='list'),
    path('provider/<int:pk>/', views.ProviderDetailView.as_view(), name='detail'),
]
