from django.contrib import admin
from .models import ProductCategory, Product


class ProductCategoryAdminView(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductAdminView(admin.ModelAdmin):
    list_display = ("name", "description", "category", "price")
    list_filter = ("category",)
    search_fields = ("name", "description", "category")
    autocomplete_fields = ("category",)


admin.site.register(ProductCategory, ProductCategoryAdminView)
admin.site.register(Product, ProductAdminView)
