from django.contrib import admin
from .models import ProductCategory, Product


class ProductCategoryAdminView(admin.ModelAdmin):
    list_display = ("name",)


class ProductAdminView(admin.ModelAdmin):
    list_display = ("name", "description", "category", "price")
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )


admin.register(ProductCategory, ProductCategoryAdminView)
admin.register(Product, ProductAdminView)
