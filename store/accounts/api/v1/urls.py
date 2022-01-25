from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api_accounts'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<str:username>/', ShowProfileView.as_view(), name='profile'),
    path('create_profile/', CreateProfileView.as_view(), name= 'create_profile'),

    path('login_phone_number/', LoginPhoneNumber.as_view(), name= 'login_phone_number'),
    path('login_phone_number_valid_code/', LoginPhoneNumberValidCode.as_view(), name= 'login_phone_number_valid_code'),
]