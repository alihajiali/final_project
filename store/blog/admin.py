from django.contrib import admin
from .models import *
from django.contrib import admin
from django.utils.html import format_html
from .models import *



admin.site.register(Comment_Post)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'market', 'like_count', 'status')
    list_filter = ('status', 'tag', 'category', 'market')
    list_editable = ('status',)
    search_fields = ('title',)