import factory
import phonenumbers
from . import models


class ProviderFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Provider

    name = factory.Faker('company')
    email = factory.Faker('email')
    phone_number = '+584243231113'
    language = factory.Faker('language_code')
    currency = factory.Faker('currency_code')
