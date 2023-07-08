from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
