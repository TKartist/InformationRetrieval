# backend/views.py

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
    global index

    def get_queryset(self):
        queryset = Vehicle.objects.all()

        # Retrieve query parameters
        search_query = self.request.query_params.get("search", None)
        brand = self.request.query_params.get("brand", None)
        model = self.request.query_params.get("model", None)
        year = self.request.query_params.get("year", None)
        min_price = self.request.query_params.get("minPrice", None)
        max_price = self.request.query_params.get("maxPrice", None)
        page = self.request.query_params.get("currentPage", 1)
        items_per_page = self.request.query_params.get("itemsPerPage", 20)

        # Apply filters if parameters are present
        if model:
            queryset = queryset.filter(model__icontains=model)

        if brand:
            queryset = queryset.filter(brand__iexact=brand)
        if year:
            queryset = queryset.filter(year=year)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        if search_query:
            textList = []
            docList = []
            jsonList = []
            queryList = []
            for vehicle in queryset:
                textList.append(vehicle.text)
                docList.append(vehicle.docno)
                json = {
                    "docno": vehicle.docno,
                    "brand": vehicle.brand,
                    "model": vehicle.model,
                    "year": vehicle.year,
                    "price": vehicle.price,
                    "text": vehicle.text,
                    "image_url": vehicle.image_url,
                    "detail_url": vehicle.detail_url,
                }
                jsonList.append(json)
            preIndex = pd.DataFrame()
            preIndex["docno"] = docList
            preIndex["text"] = textList
            q2s = [["q1", search_query]]  # q2s : Query To Send
            index = generateIndex(preIndex)
            indexedResult = getQueryResult(index, q2s, jsonList)
            queryIndex = perform_clustering(indexedResult)
            for i in queryIndex:
                queryList.append(queryset[int(i)])
            paginator = Paginator(queryList, items_per_page)
        else:
            paginator = Paginator(queryset, items_per_page)
        return paginator.get_page(page).object_list
