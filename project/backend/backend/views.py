# backend/views.py

from typing import Any
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator
from .models import Vehicle
from .serializers import VehicleSerializer
import sys
import pandas as pd

sys.path.append("../classic_cars/utilities")

from indexerScript import getQueryResult, generateIndex
from clustering import perform_clustering


class VehicleListView(ListAPIView):
    serializer_class = VehicleSerializer
    index = None
    jsons = None

    def __init__(self, *args, **kwargs):
        self.index = kwargs.pop("index", None)
        self.jsons = kwargs.pop("jsons", None)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        # Retrieve query parameters
        search_query = self.request.query_params.get("search", None)
        brand = self.request.query_params.get("brand", None)
        year = self.request.query_params.get("year", None)
        min_price = self.request.query_params.get("minPrice", None)
        max_price = self.request.query_params.get("maxPrice", None)
        page = self.request.query_params.get("currentPage", 1)
        items_per_page = self.request.query_params.get("itemsPerPage", 20)

        if search_query and search_query != "":
            queryList = []
            indexedResult = getQueryResult(self.index, search_query, self.jsons)
            if len(indexedResult.index) != 0:
                queryIndex = perform_clustering(indexedResult)
                for i in queryIndex:
                    queryList.append(queryset[int(i)])
            queryset = queryList[:]
        else:
            queryset = list(queryset)
        # Apply filters if parameters are present
        if brand:
            queryset = list(filter(lambda x: x.brand == brand, queryset))
            print(queryset)

        if year:
            queryset = list(filter(lambda x: x.year == year, queryset))

        if min_price is not None:
            queryset = list(filter(lambda x: x.price >= min_price, queryset))
        if max_price is not None:
            queryset = list(filter(lambda x: x.price <= max_price, queryset))

        paginator = Paginator(queryset, items_per_page)
        return paginator.get_page(1).object_list
