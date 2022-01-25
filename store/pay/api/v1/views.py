from django.http.response import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import *
from rest_framework import generics
from .serializers import CreateCartSerializer ,CreateCartItemSerializer, CartSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class CreateCart(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        cart = CreateCartSerializer(data=request.data)
        if cart.is_valid():
            if request.user.id == request.data['owner']:
                cart.save()
                return Response(cart.data['id'], status=status.HTTP_201_CREATED)
        return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateItemCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        item_cart = CreateCartItemSerializer(data=request.data)
        cart = Cart.objects.get(id=request.data['cart'])
        if cart.owner == request.user:
            if item_cart.is_valid():
                item_cart.save()
                product_id = item_cart.data['product']
                product = generics.get_object_or_404(Product, id=product_id)
                product.number_product -= item_cart.data['number']
                product.save()
                return Response(item_cart.data, status=status.HTTP_201_CREATED)
            return Response(item_cart.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteCartItem(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        item_cart = cart_item.objects.get(id=request.data['id'])
        cart = item_cart.cart
        if cart.owner == request.user:
            product = item_cart.product
            product.number_product += item_cart.number
            product.save()
            item_cart.delete()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(item_cart.errors, status=status.HTTP_400_BAD_REQUEST)



class EditCartItem(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        item_cart = cart_item.objects.get(id=request.data['id'])
        product = item_cart.product
        cart = item_cart.cart
        new_number = request.data['number']
        old_number = item_cart.number
        result_number = new_number - old_number
        if cart.owner == request.user:
            product.number_product -= result_number
            product.save()

            item_cart.number += result_number
            if item_cart.number == 0:
                item_cart.delete()
            else:
                item_cart.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(item_cart.errors, status=status.HTTP_400_BAD_REQUEST)



class PayCart(APIView):
    def post(self, request):
        cart = Cart.objects.get(id=request.data['id'])
        if cart.owner == request.user and cart.status == 'A':
            cart.status = 'S'
            cart.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)



class ShowOpenCart(APIView):
    def get(self, request):
        queryset = Cart.objects.filter(owner=self.request.user).filter(status = 'A')
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)



class ShowPayedCart(APIView):
    def get(self, request):
        queryset = Cart.objects.filter(owner=self.request.user).filter(status = 'S')
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)