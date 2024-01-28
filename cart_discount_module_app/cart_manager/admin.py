from django.contrib import admin

from .models import ShoppingCart


class ShoppingCartAdminView(admin.ModelAdmin):
    list_display = (
        "id",
        "total_price_pre_discount",
        "total_price_post_discount",
        "total_discounted",
        "points",
        "max_points_discount",
    )
    readonly_fields = (
        "total_price_pre_discount",
        "total_price_post_discount",
        "total_discounted",
        "max_points_discount",
    )


admin.register(ShoppingCart, ShoppingCartAdminView)
