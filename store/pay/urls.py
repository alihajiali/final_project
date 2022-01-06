from django.urls import path
from .models import Cart, cart_item
from . import views

app_name = 'pay'

urlpatterns = [
    path('<slug:slug>/show_panel/', views.Show_panel.as_view(), name='show_panel'),
    path('<slug:slug>/cart_list/', views.CartList.as_view(), name='cart_list'),
    path('status_a/', views.StatusA.as_view(), name='status_a'),
    path('status_n/', views.StatusN.as_view(), name='status_n'),
    path('status_s/', views.StatusS.as_view(), name='status_s'),
]