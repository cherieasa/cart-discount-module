from django.contrib import admin

from .models import CouponDiscount, OnTopDiscount, SeasonalDiscount


class CouponDiscountAdminView(admin.ModelAdmin):
    list_display = ("discount_type", "discount_value")
    search_fields = ("discount_type", "discount_value")


class OnTopDiscountAdminView(admin.ModelAdmin):
    list_display = ("discount_type", "discount_value", "category",)
    search_fields = ("discount_type", "discount_value")


class SeasonalDiscountAdminView(admin.ModelAdmin):
    list_display = ("every_value", "discount_value")
    search_fields = ("every_value", "discount_value")


admin.site.register(CouponDiscount, CouponDiscountAdminView)
admin.site.register(OnTopDiscount, OnTopDiscountAdminView)
admin.site.register(SeasonalDiscount, SeasonalDiscountAdminView)
