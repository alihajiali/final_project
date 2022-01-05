from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import User
from randomslugfield import RandomSlugField


class Market(models.Model):
    TYPE = (
        ('D', 'کالا های دیجیتال'),
        ('C', 'خودرو و ابزار و تجهیزات صنعتی'),
        ('M', 'مد و پوشاک'),
        ('K', 'اسباب بازی , کودک و نوزاد'),
        ('S', 'کالاهای سوپرمارکتی'),
        ('Z', 'زیبایی و سلامت'),
        ('P', 'خانه و آشپزخانه'),
        ('B', 'کتاب و لوازم تحریر و هنر'),
        ('V', 'ورزش و سفر'),
        ('H', 'محصولات بومی و محلی'),
    )
    STATUS = (
        ('A', 'تایید شده'),
        ('N', 'تایید نشده'),
        ('D', 'حذف شده'),
        ('P', 'در دست بررسی'),
    )
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name="owner_market")
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    type = models.CharField(max_length=1, choices=TYPE)

    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,blank=True,null=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Market, on_delete=CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Market, on_delete=CASCADE)

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS = (
        ('A', 'تایید شده'),
        ('N', 'تایید نشده'),
        ('D', 'حذف شده'),
        ('P', 'در دست بررسی'),
    )
    title = models.CharField(max_length=200)
    slug = RandomSlugField(length=12)
    description = models.TextField()
    price = models.IntegerField()
    market = models.ForeignKey(Market, on_delete=CASCADE)
    number_product = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)
    like = models.ManyToManyField(User, blank=True)
    like_count = models.IntegerField(default=0)
    expire = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS)

    def __str__(self):
        return self.title


class Comment_Product(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title