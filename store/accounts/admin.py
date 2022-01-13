from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from django.contrib.auth.models import Group

admin.site.register(Profile)


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('full_name', 'email', 'is_admin', 'is_seller')
	list_filter = ('is_admin', 'is_seller')
	fieldsets = (
		('Main', {'fields':('full_name', 'email', 'password')}),
		('Personal info', {'fields':('is_active', 'is_seller')}),
		('Permissions', {'fields':('is_admin',)})
	)
	add_fieldsets = (
		(None, {
			'fields':('full_name', 'email', 'password1', 'password2', 'is_seller')
		}),
	)
	search_fields = ('email', )
	ordering = ('email', )
	filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)