from rest_framework import viewsets
from .serializers import ProviderSerializer
from .models import Provider


class ProviderViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on the providers
    """
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()
