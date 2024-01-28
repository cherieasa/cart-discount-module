from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from discount_manager.models import CouponDiscount, OnTopDiscount, SeasonalDiscount
from product_manager.models import Product
from user_manager.models import User


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, null=True)
    coupon_discount = models.ForeignKey(
        CouponDiscount, on_delete=models.SET_NULL, blank=True, null=True
    )
    on_top_discount = models.ForeignKey(
        OnTopDiscount, on_delete=models.SET_NULL, blank=True, null=True
    )
    seasonal_discount = models.ForeignKey(
        SeasonalDiscount, on_delete=models.SET_NULL, blank=True, null=True
    )
    points_used = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    @property
    def total_price_post_discount(self):
        return self.calculate_total_price()

    @property
    def total_price_pre_discount(self):
        return sum(product.price for product in self.products.all())

    @property
    def total_discounted(self):
        return self.total_price_post_discount - self.total_price_pre_discount

    @property
    def max_points_discount(self):
        print("in max point")
        if (
            not self.id
            or not self.products.exists()
            or (
                self.on_top_discount
                and self.on_top_discount.discount_type == OnTopDiscount.PRODUCT_CATEGORY
            )
        ):
            return 0
        if self.coupon_discount:
            total_price = self.coupon_discount.apply_discount(
                self.total_price_pre_discount
            )
        else:
            total_price = self.total_price_pre_discount
        return min(total_price * 0.20, self.user.points)

    @property
    def remove_all_discounts(self):
        self.coupon_discount.delete()
        self.on_top_discount.delete()
        self.seasonal_discount.delete()
        self.points_used = 0
        self.save()

    def calculate_total_price(self):
        total_price = self.total_price_pre_discount

        if self.coupon_discount:
            total_price = self.coupon_discount.apply_discount(total_price)

        if (
            self.on_top_discount
            and self.on_top_discount.discount_type == OnTopDiscount.PRODUCT_CATEGORY
        ):
            total_price = self.on_top_discount.apply_discount(
                total_price, self.products
            )

        elif (
            self.points_used
            or self.on_top_discount
            and self.on_top_discount.discount_type == OnTopDiscount.POINTS
        ):
            total_price = total_price - self.points_used
            if not self.on_top_discount:
                self.on_top_discount = OnTopDiscount.objects.create(
                    discount_type=OnTopDiscount.POINTS, discount_value=self.points_used
                )
                self.on_top_discount.save()

        if self.seasonal_discount:
            total_price = self.seasonal_discount.apply_discount(total_price)

        return total_price

    def save(self, *args, **kwargs):
        if (
            self.on_top_discount
            and self.on_top_discount.discount_type == OnTopDiscount.PRODUCT_CATEGORY
            and self.points_used
        ):
            raise ValidationError("Cannot use more than one on top discount.")
        if self.points_used > self.max_points_discount:
            raise ValidationError(
                f"Cannot redeem more than {self.max_points_discount} points."
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")
