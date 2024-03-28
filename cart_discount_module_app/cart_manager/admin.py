from django.contrib import admin

from .models import ShoppingCart


class ShoppingCartAdminView(admin.ModelAdmin):
    autocomplete_fields = (
        "user",
        "coupon_discount",
        "on_top_discount",
        "seasonal_discount",
    )
    list_display = (
        "id",
        "user",
        "points_used",
    )
    readonly_fields = (
        "total_price_post_discount",
        "max_points_discount",
        "total_discounted",
        "total_price_pre_discount",
    )
    filter_horizontal = [
        "products",
    ]
    fields = (
        "user",
        "points_used",
        "max_points_discount",
        "products",
        "coupon_discount",
        "on_top_discount",
        "seasonal_discount",
        "total_price_pre_discount",
        "total_discounted",
        "total_price_post_discount",
    )


admin.site.register(ShoppingCart, ShoppingCartAdminView)
