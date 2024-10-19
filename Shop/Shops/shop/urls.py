from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_shop, name='register_shop'),
    path('search/', views.search_shops, name='search_shops'),
    path('api/shops/register/', views.api_register_shop, name='api_register_shop'),
    path('api/shops/search/', views.api_search_shops, name='api_search_shops'),
    path('', views.register_shop, name='home'),
]
