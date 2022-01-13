from django.http.response import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import *
from rest_framework import generics
from .serializers import CreateCartSerializer ,CreateCartItemSerializer, DeleteCartItemSerializer
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
    # permission_classes = [IsAuthenticated, ]
    def post(self, request):
        item_cart = CreateCartItemSerializer(data=request.data)
        if item_cart.is_valid():
            item_cart.save()
            product_id = item_cart.data['product']
            product = generics.get_object_or_404(Product, id=product_id)
            product.number_product -= item_cart.data['number']
            product.save()
            return Response(item_cart.data, status=status.HTTP_201_CREATED)
        return Response(item_cart.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteCartItem(APIView):
    # def get(self, request, pk):
    #     item = cart_item.objects.get(id=pk)
    #     print("&"*80, item.number)
    #     product_id = item.product
    #     print("&"*80, product_id)
    #     product = generics.get_object_or_404(Product, id=product_id)
    #     print("&"*80, product)
    #     print("&"*80, product.number_product)
    #     product.number_product += item.number
    #     print("&"*80, product.number_product)
    #     product.save()
    #     item.delete()
    #     return Response({"message":"ok"}, status=status.HTTP_200_OK)
    def post(self, request):
        item_cart = DeleteCartItemSerializer(data=request.data)
        if item_cart.is_valid():
            print("*"*80, item_cart)
            item_cart.delete()
            product_id = item_cart.data['product']
            product = generics.get_object_or_404(Product, id=product_id)
            product.number_product += item_cart.data['number']
            product.save()
            return Response(item_cart.data, status=status.HTTP_201_CREATED)
        return Response(item_cart.errors, status=status.HTTP_400_BAD_REQUEST)
