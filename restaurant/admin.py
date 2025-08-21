from django.contrib import admin
from .models import Meal, OrderTransction
# Register your models here.

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'price', 'available', 'images',
    )

    search_fields = ('name', 'description',)


@admin.register(OrderTransction)
class OrderTransctionAdmin(admin.ModelAdmin):
    list_display = (
        'meal', 'customer', 'amount', 'status', 'created_at',
    )

    search_fields = ('meal', 'customer',)

