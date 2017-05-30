from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from faker import Faker

from providers.models import Provider
from . import factories, serializers


class ProviderCreateTest(APITestCase):
    """
    Test class for testing the creation of a provider
    """

    def test_create_provider(self):
        """
        Ensure that a provider is created on a post request
        """
        url = reverse('provider-list')
        provider = factories.ProviderFactory.build()
        serializer = serializers.ProviderSerializer(provider)
        response = self.client.post(url, serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 1)

        # Checks that the response has the info about the provider. The response data id on the data is changed to None
        # To allow comparison with the serializer (it doesn't have an id)
        response.data['id'] = None
        self.assertEqual(response.data, serializer.data)


class ProviderViewSetTest(APITestCase):
    """
    Test class to test the Provider view set (without creation)
    """

    def __init__(self, *args, **kwargs):
        self.fake = Faker()
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.provider = factories.ProviderFactory.create()
        self.serializer = serializers.ProviderSerializer(self.provider)

    def test_provider_list(self):
        """
        Test the list view for the providers
        """
        # Creating a few providers
        instances = [factories.ProviderFactory.build() for _ in range(20)]
        Provider.objects.bulk_create(instances)

        # Making the request
        url = reverse('provider-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), Provider.objects.count())

        for provider, provider_instance in zip(response.data, Provider.objects.all()):
            serializer = serializers.ProviderSerializer(provider_instance)
            self.assertEqual(provider, serializer.data)

    def test_provider_detail(self):
        """
        Tests the detail data for a provider
        """
        url = reverse('provider-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.data, self.serializer.data)

    def test_provider_update(self):
        """
        Tests the update methods (partial and complete) for the providers
        """
        url = reverse('provider-detail', kwargs={'pk': 1})

        # Partial update
        new_name = self.fake.company()
        response = self.client.patch(url, {'name': new_name}, format='json')
        self.assertEqual(response.data['name'], new_name)

        # Complete update
        new_provider = factories.ProviderFactory.build()
        serializer = serializers.ProviderSerializer(new_provider)
        response = self.client.put(url, serializer.data, format='json')

        response.data['id'] = None
        self.assertEqual(response.data, serializer.data)

    def test_provider_delete(self):
        """
        Tests the delete method on the provider endpoint 
        """
        url = reverse('provider-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
