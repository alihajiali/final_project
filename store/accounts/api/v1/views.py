from rest_framework.views import APIView
from ...models import Profile, User
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response


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





#profile

class ShowProfileView(APIView):
    def get(self, request, username):
        profile = Profile.objects.get(username=username)
        serializer = ProfileSerializer(instance=profile)
        return Response(serializer.data)

class CreateProfileView(APIView):
    def post(self, request):
        print(request.binary)
        # data = ProfileSerializer(data=request.data)
        # if data.is_valid():
        #     print('*'*80, data)
        # else:
        #     print('*'*80, data)
        #     print('*'*80, request.data)