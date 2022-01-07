from django.contrib import admin
from .models import *
from django.contrib import admin
from django.utils.html import format_html
from .models import cart_item, Cart


@admin.register(cart_item)
class cart_itemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'number', 'price')
    list_filter = ('number',)
    search_fields = ('cart',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'market', 'created', 'updated', 'status')
    list_filter = ('market', 'status', 'owner')
    list_editable = ('status',)
    search_fields = ('title', 'owner')
