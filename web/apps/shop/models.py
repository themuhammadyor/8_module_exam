from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.shared.models import AbstractBaseModel
from apps.users.models import User


class Category(AbstractBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover = models.ImageField(upload_to='categories/')


class SubCategory(AbstractBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_slug = models.ForeignKey('Category', on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='categories/')


class Brand(AbstractBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover = models.ImageField(upload_to='brands/')


class Product(AbstractBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    brand_slug = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_slug = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover = models.ImageField(upload_to='products/')
    published_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    like_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    objects = models.Manager()


class ProductReview(AbstractBaseModel):
    product_slug = models.ForeignKey('Product', on_delete=models.CASCADE)
    user_slug = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    like_count = models.IntegerField(default=0)


class Favorite(AbstractBaseModel):
    product_slug = models.ForeignKey('Product', on_delete=models.CASCADE)
    user_slug = models.ForeignKey('User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Favourite: {self.product.name}'


class Cart(AbstractBaseModel):
    product_slug = models.ForeignKey('Product', on_delete=models.CASCADE)
    user_slug = models.ForeignKey('User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Card: {self.product_slug.name}'
