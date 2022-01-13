from django.http.response import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import *
from rest_framework import generics
from .serializers import CreateCartSerializer ,CreateCartItemSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class CreateCart(APIView):
    # permission_classes = [IsAuthenticated, ]
    def post(self, request):
        cart = CreateCartSerializer(data=request.data)
        if cart.is_valid():
            cart.save()
            return Response(cart.data['id'], status=status.HTTP_201_CREATED)
        return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateItemCart(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        item_cart = CreateCartItemSerializer(data=request.data)
        if item_cart.is_valid():
            item_cart.save()
            return Response(item_cart.data, status=status.HTTP_201_CREATED)
        return Response(item_cart.errors, status=status.HTTP_400_BAD_REQUEST)