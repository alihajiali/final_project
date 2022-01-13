from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from ...models import *

class MarketSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    class Meta:
        model = Market
        fields = '__all__'


class TypeMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('title', 'type')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'