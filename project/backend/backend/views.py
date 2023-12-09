# backend/views.py

from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleListView(ListAPIView):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = Vehicle.objects.all()

        # Retrieve query parameters
        search_query = self.request.query_params.get('search', None)
        brand = self.request.query_params.get('brand', None)
        model = self.request.query_params.get('model', None)
        year = self.request.query_params.get('year', None)
        min_price = self.request.query_params.get('minPrice', None)
        max_price = self.request.query_params.get('maxPrice', None)
        page = self.request.query_params.get('currentPage', 1 )
        items_per_page = self.request.query_params.get('itemsPerPage', 20)

        # Apply filters if parameters are present
        if search_query:
            queryset = queryset.filter(description__icontains=search_query )
        
        if model:
            queryset = queryset.filter(description__icontains=model)
        if brand:
            queryset = queryset.filter(brand=brand)
        if year:
            queryset = queryset.filter(year=year)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

    
        paginator = Paginator(queryset, items_per_page)
        return paginator.get_page(page).object_list
