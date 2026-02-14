from django.views.generic import ListView, TemplateView ,DetailView
from django.db.models import Q
from .models import ProviderProfile, Category

class HomeView(TemplateView):
    template_name = 'home.html'  # <--- POINTS TO src/templates/home.html

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        #fetch all catergoies to display as icons (eg. plumber, maid)
        context['categories']= Category.objects.all()
        return context

    
class ProviderListView(ListView):
    template_name = 'providers/list.html' # <--- POINTS TO src/templates/providers/list.html
    model = ProviderProfile
    context_object_name = 'providers'
    paginate_by = 20

    def get_queryset(self):
        # # Start with all providers (or maybe just verified ones later)
        queryset = ProviderProfile.objects.all().select_related('category')
        category_slug = self.request.GET.get('category')

        # 1. Filter by Category (e.g. ?category=plumber)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # 2. Filter by Township (e.g. ?town=Muse)
        town = self.request.GET.get('town')
        if town and town != "":
            queryset = queryset.filter(township=town)

        # 3. Text Search (e.g. ?q=John)
        # We use Q objects to search across multiple fields at once
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(business_name__icontains=query) |  #icontains: matches "john", "John", "JOHN".
                Q(phone_number__icontains=query) |
                Q(description__icontains=query)
            )
            
        # Order by verification status (Verified first), then newness
        return queryset.order_by('-is_verified', '-id')

    def get_context_data(self, **kwargs):
        """
        Pass the search terms back to the template so we can 
        pre-fill the search bar.
        """
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.request.GET.get('category', '')
        context['current_town'] = self.request.GET.get('town', 'Muse')
        context['current_query'] = self.request.GET.get('q', '')
        return context
        
class ProviderDetailView(DetailView):
    template_name = 'providers/detail.html'
    model = ProviderProfile
    context_object_name = 'provider' # change template name /check this template html