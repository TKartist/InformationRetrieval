"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# backend/urls.py

from django.urls import path
from .views import VehicleListView
from .models import Vehicle
import pandas as pd
import sys

sys.path.append("../classic_cars/utilities")
from indexerScript import generateIndex

queryset = Vehicle.objects.all()
queryList = []
textList = []
docList = []
jsons = []
preIndex = pd.DataFrame()
for vehicle in queryset:
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
    jsons.append(json)
    textList.append(vehicle.text)
    docList.append(vehicle.docno)
preIndex["docno"] = docList
preIndex["text"] = textList
index = generateIndex(preIndex)

urlpatterns = [
    path(
        "api/vehicles/",
        VehicleListView.as_view(index=index, jsons=jsons),
        name="vehicle_list",
    ),
]
