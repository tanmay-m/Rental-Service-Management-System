from django.shortcuts import render

# Create your views here.
# search/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import Car

@csrf_exempt
def add_car(request):
    if request.method == 'POST':
        # Retrieve the car details from the request data
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        owner = request.POST.get('owner')
        rating = request.POST.get('rating')
        distance = request.POST.get('distance')

        # Create a new car object and save it to the database
        car = Car(name=name, brand=brand, category=category, owner=owner, rating=rating, distance=distance)
        car.save()

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    else:
        # Return a JSON response indicating error if the request method is not POST
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@require_GET
def search_cars(request):
    ratings = request.GET.get('ratings')
    distance = request.GET.get('distance')
    owner = request.GET.get('owner')
    category = request.GET.get('category')
    brand = request.GET.get('brand')

    cars = Car.objects.all()
    if ratings:
        cars = cars.filter(ratings=ratings)
    if distance:
        cars = cars.filter(distance=distance)
    if owner:
        cars = cars.filter(owner__icontains=owner)
    if category:
        cars = cars.filter(category__icontains=category)
    if brand:
        cars = cars.filter(brand__icontains=brand)

    data = {
        'cars': [
            {
                'id': car.id,
                'name': car.name,
                'ratings': car.ratings,
                'distance': car.distance,
                'owner': car.owner,
                'category': car.category,
                'brand': car.brand,
            }
            for car in cars
        ]
    }
    return JsonResponse(data)
