from django.contrib import admin
from .models import *

# admin.site.register(Market)
# admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Product)
admin.site.register(Comment_Product)


from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Tag, Comment_Product, Market


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'owner')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('title',)
    actions = ('make_confirmed',)

    def make_confirmed(self, request, queryset):
        rows = queryset.update(status='A')
        self.message_user(request, f'{rows} بروز شد')
    make_confirmed.short_description = 'انتخاب شده ها تایید شوند'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     list_filter = ('title',)
#     search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'images_tag')
    list_filter = ('status',)
    list_editable = ('price',)
    # raw_id_fields = ('category',)
    actions = ('make_available',)

    def images_tag(self, obj):
        return format_html('<img src="{}" width="60" height="60" />'.format(obj.image.url))

    images_tag.short_description = 'Image'

    def make_available(self, request, queryset):
        rows = queryset.update(available=True)
        self.message_user(request, f'{rows} Updated')
    make_available.short_description = 'make all available'