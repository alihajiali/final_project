from django.db.models import fields
from rest_framework import serializers
from ...models import *



class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_item
        fields = "__all__"

    def create(self, validate_data):
        item = cart_item.objects.create(**validate_data)
        return item


class CreateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

    def create(self, validate_data):
        cart = Cart.objects.create(**validate_data)
        return cart


class DeleteCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_item
        fields = "__all__"