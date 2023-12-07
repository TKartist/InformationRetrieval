from django.urls import path
from .views import vehicle_list

urlpatterns = [
    path('api/vehicles/', vehicle_list, name='vehicle_list'),
]
