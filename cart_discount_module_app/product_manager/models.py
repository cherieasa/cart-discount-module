from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} / {self.price}"

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
