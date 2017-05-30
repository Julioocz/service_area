from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    language = models.CharField(max_length=3)
    currency = models.CharField(max_length=3)