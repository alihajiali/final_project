from django.http.response import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import *
from rest_framework import generics
from .serializers import MarketSerializer, TypeMarketSerializer, ProductSerializer


# all market   :    127.0.1:8000/api/v1    :method    ->      get
class AllMarketView(viewsets.ViewSet):
    def list(self, request):
        queryset = Market.objects.filter(status='A')
        serializer = MarketSerializer(queryset, many=True)
        return Response(serializer.data)



# all market   :    127.0.1:8000/api/v1/(typ)    :method    ->      get
class FilterTypeMarketView(APIView):
    def get(self, request, typ):
        queryset = Market.objects.filter(status='A', type=typ)
        serializer = MarketSerializer(queryset, many=True)
        return Response(serializer.data)
# typ{
    # ('D', 'کالا های دیجیتال'),
    # ('C', 'خودرو و ابزار و تجهیزات صنعتی'),
    # ('M', 'مد و پوشاک'),
    # ('K', 'اسباب بازی , کودک و نوزاد'),
    # ('S', 'کالاهای سوپرمارکتی'),
    # ('Z', 'زیبایی و سلامت'),
    # ('P', 'خانه و آشپزخانه'),
    # ('B', 'کتاب و لوازم تحریر و هنر'),
    # ('V', 'ورزش و سفر'),
    # ('H', 'محصولات بومی و محلی'),
# }


# class TypeMarket(APIView):
#     def get(self, request):
#         typ = (
#             {'D': 'کالا های دیجیتال'},
#             {'C': 'خودرو و ابزار و تجهیزات صنعتی'},
#             {'M': 'مد و پوشاک'},
#             {'K': 'اسباب بازی , کودک و نوزاد'},
#             {'S': 'کالاهای سوپرمارکتی'},
#             {'Z': 'زیبایی و سلامت'},
#             {'P': 'خانه و آشپزخانه'},
#             {'B': 'کتاب و لوازم تحریر و هنر'},
#             {'V': 'ورزش و سفر'},
#             {'H': 'محصولات بومی و محلی'},
#         )
#         return Response(typ)


class TypeMarket(APIView):
    def get(self, request):
        queryset = Market.objects.all()
        l = []
        for query in queryset:
            if query in l:
                continue
            else:
                l.append(query)

        serialize = TypeMarketSerializer(l, many=True)
        return Response(serialize.data)



class AllProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.filter(status='A', number_product__gt=0)



class TagFilterProduct(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        tag = self.kwargs['tag']
        return Product.objects.filter(status='A', tag=tag, number_product__gt=0)



class PriceFilterProduct(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        min = self.kwargs['min']
        max = self.kwargs['max']
        return Product.objects.filter(status='A', price__gte=min, price__lte=max, number_product__gt=0)




class AvailibleFilterProduct(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        if self.kwargs['status'] == 'availible':
            return Product.objects.filter(status='A', number_product__gt=0)
        elif self.kwargs['status'] == 'not_availible':
            return Product.objects.filter(status='A', number_product = 0)
