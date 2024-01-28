from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from discount_manager.models import CouponDiscount, OnTopDiscount, SeasonalDiscount
from product_manager.models import Product
from user_manager.models import User


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    coupon_discount = models.ForeignKey(
        CouponDiscount, on_delete=models.SET_NULL, blank=True, null=True
    )
    on_top_discount = models.ForeignKey(
        OnTopDiscount, on_delete=models.SET_NULL, blank=True, null=True
    )
    seasonal_discount = models.ForeignKey(
        SeasonalDiscount, on_delete=models.SET_NULL, blank=True, null=True
    )
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def calculate_total_price(self):
        total_price = self.total_price_pre_discount

        if self.coupon_discount:
            total_price = self.coupon_discount.apply_discount(total_price)

        if self.on_top_discount:
            total_price = self.on_top_discount.apply_discount(
                total_price, self.products
            )

        if self.seasonal_discount:
            total_price = self.seasonal_discount.apply_discount(total_price)

        return total_price

    @property
    def total_price_pre_discount(self):
        return sum(product.price for product in self.products.all())

    @property
    def total_price_post_discount(self):
        return self.calculate_total_price()

    @property
    def total_discounted(self):
        return self.total_price_pre_discount - self.total_price_post_discount

    @property
    def max_points_discount(self):
        if self.coupon_discount:
            total_price_after_coupon = self.coupon_discount.apply_discount(
                self.total_price_pre_discount
            )
            return min(total_price_after_coupon * 0.20, self.user.points)
        return None

    def save(self, *args, **kwargs):
        if self.points > self.max_points_discount:
            raise ValidationError(
                "Points used cannot exceed 20% of the total price after coupon discount."
            )

        super().save(*args, **kwargs)
