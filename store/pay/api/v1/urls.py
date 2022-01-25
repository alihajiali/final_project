from django.urls import path, re_path
from django.urls.conf import include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('', CreateCart, basename='create_cart')

app_name = 'api'

urlpatterns = [
    # path('', include(router.urls)),
    path('CreateCart/', CreateCart.as_view()),
    path('CreateItemCart/', CreateItemCart.as_view()),
    path('DeleteCartItem/', DeleteCartItem.as_view()),
    path('EditCartItem/', EditCartItem.as_view()),

    path('PayCart/', PayCart.as_view()),

    path('ShowOpenCart/', ShowOpenCart.as_view()),
    path('ShowPayedCart/', ShowPayedCart.as_view()),
]