from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

from main_app.managers import ProductManager


# Create your models here.


class CreationDateMixin(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract=True


class Profile(CreationDateMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15
    )

    address = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    objects = ProductManager()


class Product(CreationDateMixin):
    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    in_stock = models.PositiveIntegerField()

    is_available = models.BooleanField(
        default=True
    )


class Order(CreationDateMixin):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    products = models.ManyToManyField(
        to=Product
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    is_completed = models.BooleanField(
        default=False
    )
