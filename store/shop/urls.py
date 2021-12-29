from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('create-shop', views.CreateShop.as_view(), name='create_market'),
]