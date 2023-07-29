from django.urls import path
from .views import add_car,search_cars

urlpatterns = [
    path('add-car/', add_car, name='add_car'),
    path('', search_cars, name='search_cars'),
]
