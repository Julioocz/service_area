import factory
from django.contrib.gis.geos import Polygon

from . import models


class ProviderFactory(factory.DjangoModelFactory):
    name = factory.Faker('company')
    email = factory.Faker('email')
    phone_number = '+584243231113'
    language = factory.Faker('language_code')
    currency = factory.Faker('currency_code')

    class Meta:
        model = models.Provider


class ServiceAreaFactory(factory.DjangoModelFactory):
    name = factory.Faker('street_name')
    price = factory.Faker('pyfloat', positive=True)
    area = Polygon(((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)))
    provider = factory.SubFactory(ProviderFactory)

    class Meta:
        model = models.ServiceArea
