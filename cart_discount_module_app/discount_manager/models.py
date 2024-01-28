from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from product_manager.models import ProductCategory


class CouponDiscount(models.Model):
    FIXED_AMOUNT = "fixed_amount"
    PERCENTAGE = "percentage"

    DISCOUNT_TYPE_CHOICES = [
        (FIXED_AMOUNT, "Fixed Amount"),
        (PERCENTAGE, "Percentage"),
    ]

    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def apply_discount(self, total_price):
        if total_price > 0:
            if self.discount_type == self.FIXED_AMOUNT:
                return total_price - self.discount_value
            elif self.discount_type == self.PERCENTAGE:
                return total_price * (1 - self.discount_value / 100)
            else:
                raise ValueError("Invalid discount type")
        return 0

    def __str__(self):
        return f"{self.discount_type} - {self.discount_value}"


class OnTopDiscount(models.Model):
    PRODUCT_CATEGORY = "product_category"
    POINTS = "points"

    DISCOUNT_TYPE_CHOICES = [
        (PRODUCT_CATEGORY, "Fixed Amount"),
        (POINTS, "Points"),
    ]

    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.FloatField(default=0, validators=[MinValueValidator(0)])
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    @property
    def points(self):
        if self.discount_type == self.POINTS:
            from cart_manager.models import ShoppingCart

            return ShoppingCart.objects.filter(on_top_discount=self).points
        return None

    def apply_discount(self, total_price, products_queryset):
        if self.discount_type == self.PRODUCT_CATEGORY:
            total_category_price = sum(
                product.price
                for product in products_queryset.filter(category=self.category)
            )
            discount = total_category_price * (1 - self.discount_value / 100)
        elif self.discount_type == self.POINTS:
            discount = self.points
        else:
            raise ValueError("Invalid discount type")

        return total_price - discount

    def __str__(self):
        if self.discount_type == self.PRODUCT_CATEGORY:
            return f"{self.discount_type} / {self.category} - {self.discount_value}"
        elif self.discount_type == self.POINTS:
            return f"{self.discount_type} / {self.points}"
        return None


class SeasonalDiscount(models.Model):
    every_value = models.FloatField(default=0, validators=[MinValueValidator(0)])
    discount_value = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        if self.discount_value > self.every_value:
            raise ValidationError(
                'Discount value cannot be greater than minimum "every" value.'
            )

        super().save(*args, **kwargs)
