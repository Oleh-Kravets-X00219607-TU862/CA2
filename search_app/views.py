from shop.models import Product, Category
from django.views.generic import ListView
from django.db.models import Q

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        available = self.request.GET.get('available', '')

        filters = Q(name__icontains=query) | Q(description__icontains=query)

        if category:
            filters &= Q(category__id=category)
        if min_price:
            filters &= Q(price__gte=min_price)
        if max_price:
            filters &= Q(price__lte=max_price)
        if available:
            filters &= Q(available=available == 'true')

        return Product.objects.filter(filters)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['categories'] = Category.objects.all()
        return context


