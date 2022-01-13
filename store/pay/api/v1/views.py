from django.http.response import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import *
from rest_framework import generics
from .serializers import CreateCartItemSerializer
# from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated



class CreateCart(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        product = Product.objects.get(id=request.data['product'])
        print("^"*80, request.data['product'])



# class CreateCart(APIView):
#     def get(self, request):
