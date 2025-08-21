from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


DELIVERY_STATUS_CHOICES = (
    ("pending", "PENDING"),
    ("failed", "FAILED"),
    ("completed", "COMPLETED"),
)
# Create your models here.

class Meal(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField("price ($)", max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='meal_images', default='meal_images/default_meal.jpg')
    available = models.BooleanField(default=False)
    stock = models.IntegerField("stock count", db_default=0)


    def __str__(self):
        return self.description


class OrderTransction(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField("amount paid($)", max_digits=64, decimal_places=2, default=0)

    status = models.CharField("delivery status", max_length=9, choices=DELIVERY_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField("date created", default=now)