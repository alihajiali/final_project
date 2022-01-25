from django.forms import ValidationError
from rest_framework.views import APIView
from ...models import Profile, User
from .serializers import (
    RegisterSerializer, 
    ProfileSerializer, 
    LoginPhoneNumberSerializer, 
    LoginPhoneNumberSerializerValidCode
)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import  AllowAny
from kavenegar import *
import random
import time
import redis
from django.conf import settings


# register

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# 127.0.1:8000/api_accounts/v1/register/     ->    method:post
# {
#     "email": "",
#     "full_name": "",
#     "phone_number": "",
#     "password": "",
#     "password2": ""
# }


# login

# 127.0.1:8000/api_accounts/v1/token/             ->    method:post
# 127.0.1:8000/api_accounts/v1/token/refresh/     ->    method:post
# {
#     "email": "",
#     "password": ""
# }


# profile

class ShowProfileView(APIView):
    def get(self, request, username):
        profile = Profile.objects.get(username=username)
        serializer = ProfileSerializer(instance=profile)
        return Response(serializer.data)




class CreateProfileView(APIView):
    def post(self, request):
        file_serializer = ProfileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(user = request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 127.0.1:8000/api_accounts/v1/create_profile/     -> method : POST




redis_cli = redis.Redis()

class LoginPhoneNumber(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        phone_number = LoginPhoneNumberSerializer(data=request.data)
        if phone_number.is_valid():
            number = str(phone_number.data['phone_number'])
            user = User.objects.filter(phone_number=number)
            if not user.exists():
                return Response({'message': 'This phone number does not exists !!!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                rand_num = random.randint(11111, 99999)
                api = KavenegarAPI('79714A78714F5A56684B58706E5968345154444F4F386B78464148452F66476A694F6C7546594C466965633D')
                params = { 'sender' : '', 'receptor': '09'+number, 'message' : f'سلام ; کد شما : \n{rand_num}'}
                redis_cli.set(f'09{number}', rand_num, 120)
                # response = api.sms_send( params)
                return Response(f'09{number} - {user} - {rand_num}', status=status.HTTP_201_CREATED)





class LoginPhoneNumberValidCode(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        phone_number = LoginPhoneNumberSerializerValidCode(data=request.data)
        if phone_number.is_valid():
            number = str(phone_number.data['phone_number'])
            code = str(phone_number.data['code'])
            user = User.objects.get(phone_number=number)
            token = RefreshToken.for_user(user)
            if code == str(redis_cli.get("09395242203").decode()):
                return Response(data={"refresh":str(token), 'access':str(token.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response(phone_number.errors, status=status.HTTP_400_BAD_REQUEST) 
            