from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.deletion import CASCADE
from .managers import MyUserManager


class User(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True)
	full_name = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=9, unique=True, blank=True, null=True)
	is_admin = models.BooleanField(default=False)
	is_seller = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	objects = MyUserManager()
	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['full_name', 'phone_number']

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
	username = models.CharField(max_length=200, unique=True)
	address = models.TextField()
	image = models.ImageField(upload_to='profile/%Y/%m/%d/')

	def __str__(self):
		return self.username
