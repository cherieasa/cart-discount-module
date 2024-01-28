from django.contrib import admin

from .models import CouponDiscount, OnTopDiscount, SeasonalDiscount


class CouponDiscountAdminView(admin.ModelAdmin):
    list_display = ("discount_type", "discount_value")


class OnTopDiscountAdminView(admin.ModelAdmin):
    list_display = ("discount_type", "discount_value", "category", "points")


class SeasonalDiscountAdminView(admin.ModelAdmin):
    list_display = ("every_value", "discount_value")


admin.register(CouponDiscount, CouponDiscountAdminView)
admin.register(OnTopDiscount, OnTopDiscountAdminView)
admin.register(SeasonalDiscount, SeasonalDiscountAdminView)
