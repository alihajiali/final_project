from django.urls import path, re_path
from django.urls.conf import include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', CreateCart, basename='create_cart')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    # path('product/<int:id>', CreateCart.as_view())
]