from django.urls import path, re_path
from django.urls.conf import include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', AllMarketView, basename='all_market')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('<str:typ>', FilterTypeMarketView.as_view(), name='filter_type_market'),
    path('type_market/', TypeMarket.as_view(), name='type_market'),

    path('all_product/', AllProductView.as_view()),
    path('tag/<tag>/', TagFilterProduct.as_view()),
    path('price/<min>&<max>/', PriceFilterProduct.as_view()),
    # path('<status>/', AvailibleFilterProduct.as_view()),
]