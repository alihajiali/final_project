from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.login.as_view(), name='login'),
    path('register', views.register.as_view(), name='register'),
    path('logout', views.log_out.as_view(), name='log_out'),
    path('profile/', views.profile.as_view(), name='profile'),
]