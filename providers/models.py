from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    language = models.CharField(max_length=3)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f'Provider {self.name}'


class ServiceArea(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    area = models.PolygonField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='service_areas')

    def __str__(self):
        return f'Service area {self.name} from provider {self.provider.name}'
