from django.db.models import fields
from rest_framework import serializers
from ...models import *



class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_item
        fields = ("product", )