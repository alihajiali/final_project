from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.login.as_view(), name='login'),
    path('register', views.register.as_view(), name='register'),
    path('logout', views.log_out.as_view(), name='log_out'),
    path('profile/', views.profile.as_view(), name='profile'),
    #shop
    path('create-shop', views.CreateShop.as_view(), name='create_market'),
    path('edit-shop/<slug:slug>/', views.EditShop.as_view(), name='edit_market'),
    path('delete-shop/<slug:slug>/', views.DeleteShop.as_view(), name='delete_market'),
]