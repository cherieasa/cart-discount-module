# Generated by Django 4.2.6 on 2024-01-28 11:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_manager', '0001_initial'),
        ('discount_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('coupon_discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discount_manager.coupondiscount')),
                ('on_top_discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discount_manager.ontopdiscount')),
                ('products', models.ManyToManyField(to='product_manager.product')),
                ('seasonal_discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discount_manager.seasonaldiscount')),
            ],
        ),
    ]