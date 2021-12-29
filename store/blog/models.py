from django.db import models
from accounts.models import User
from shop.models import Market, Category, Tag
from randomslugfield import RandomSlugField
from django.db.models.deletion import CASCADE


class Post(models.Model):
    STATUS = (
        ('A', 'تایید شده'),
        ('N', 'تایید نشده'),
        ('D', 'حذف شده'),
        ('P', 'در دست بررسی'),
    )
    title = models.CharField(max_length=200)
    slug = RandomSlugField(length=10)
    description = models.TextField()
    Weblog = models.ForeignKey(Market, on_delete=CASCADE)
    images = models.FileField()
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)
    like = models.ManyToManyField(User, blank=True)
    like_count = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS)

    def __str__(self):
        return self.title


class Comment_Post(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title