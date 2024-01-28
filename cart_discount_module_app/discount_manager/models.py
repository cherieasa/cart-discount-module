from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    class Meta:
        verbose_name = _("Coupon Discount")
        verbose_name_plural = _("Coupon Discounts")


class OnTopDiscount(models.Model):
    PRODUCT_CATEGORY = "product_category"
    POINTS = "points"

    DISCOUNT_TYPE_CHOICES = [
        (PRODUCT_CATEGORY, "Product Category"),
        (POINTS, "Points"),
    ]

    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter value in percentage eg. 50 for 50%",
    )
    category = models.ForeignKey(
        ProductCategory, blank=True, null=True, on_delete=models.CASCADE
    )

    def apply_discount(self, total_price, products_queryset):
        if self.discount_type == self.PRODUCT_CATEGORY:
            total_category_price = sum(
                product.price
                for product in products_queryset.filter(category=self.category)
            )
            print("total cat price", total_category_price)
            discount = total_category_price * (1 - self.discount_value / 100)

        return total_price - discount

    def __str__(self):
        if self.discount_type == self.PRODUCT_CATEGORY:
            return f"{self.discount_type} / {self.category} - {self.discount_value}"
        elif self.discount_type == self.POINTS:
            return f"{self.discount_type} / {self.points}"
        return None

    def save(self, *args, **kwargs):
        if self.discount_type == self.PRODUCT_CATEGORY and not self.category:
            raise ValidationError(
                "Category cannot be blank for discount type 'product_category'."
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("On Top Discount")
        verbose_name_plural = _("On Top Discounts")


class SeasonalDiscount(models.Model):
    every_value = models.FloatField(default=0, validators=[MinValueValidator(0)])
    discount_value = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def apply_discount(self, total_price):
        if self.every_value == 0 or self.discount_value == 0:
            return total_price

        discount_applied = (total_price // self.every_value) * self.discount_value
        return total_price - discount_applied

    def save(self, *args, **kwargs):
        if self.discount_value > self.every_value:
            raise ValidationError(
                'Discount value cannot be greater than minimum "every" value.'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Every {self.every_value} spent, discount {self.discount_value}"

    class Meta:
        verbose_name = _("Seasonal Discount")
        verbose_name_plural = _("Seasonal Discounts")
