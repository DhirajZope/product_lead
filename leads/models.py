from django.db import models
from common_utils.fields import PhoneNumberField
from products.models import Product


# Create your models here.

class Lead(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    interested_products = models.ManyToManyField(
        Product,
        related_name="leads",
        related_query_name="lead"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
