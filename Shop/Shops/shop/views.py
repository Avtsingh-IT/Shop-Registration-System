from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ShopRegistrationForm  
from .models import Shop
import math
from rest_framework.decorators import api_view
from rest_framework.response import Response

def search_shops(request):
    if request.method == 'GET':
        user_lat = request.GET.get('latitude')
        user_lon = request.GET.get('longitude')

        if user_lat is None or user_lon is None:
            # If latitude or longitude is missing, show the search form
            return render(request, 'shop/search.html')  # Ensure you have a search.html template to take user input

        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            return HttpResponse("Invalid latitude or longitude values", status=400)

        shops = Shop.objects.all()
        shop_distances = []

        for shop in shops:
            if shop.latitude is not None and shop.longitude is not None:
                distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
                shop_distances.append((shop, distance))

        # Sort shops by distance
        shop_distances.sort(key=lambda x: x[1])

        return render(request, 'shop/search_results.html', {'shop_distances': shop_distances})
    
    return HttpResponse("Invalid request method", status=405)


def register_shop(request):
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Shop registered successfully!")
    else:
        form = ShopRegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers


@api_view(['GET', 'POST'])
def api_register_shop(request):
    if request.method == 'POST':
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Shop registered successfully!'})
        return Response(serializer.errors, status=400)

    shops = Shop.objects.all()
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_search_shops(request):
    user_lat = request.GET.get('latitude')
    user_lon = request.GET.get('longitude')

    if user_lat is None or user_lon is None:
        return Response({'error': 'Latitude and longitude are required.'}, status=400)

    try:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
    except ValueError:
        return Response({'error': 'Invalid latitude or longitude values.'}, status=400)

    shops = Shop.objects.all()
    shop_distances = []

    for shop in shops:
        if shop.latitude is not None and shop.longitude is not None:
            distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
            shop_distances.append({'shop': ShopSerializer(shop).data, 'distance': distance})

    # Sort shops by distance
    shop_distances.sort(key=lambda x: x['distance'])

    return Response(shop_distances)
