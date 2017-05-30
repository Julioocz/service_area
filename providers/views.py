import logging

from django.views.decorators.cache import cache_page
from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProviderSerializer, ServiceAreaSerializer
from .models import Provider, ServiceArea

logger = logging.getLogger(__name__)


class ProviderViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on the providers
    
    list: Retrieves a list of providers
    create: Creates a new provider
    retrieve: Retrieves an specific provider
    delete: Deletes an specific provider
    partial_update: Allows to update a provider partially
    update: Allows to update a provider completely
    """
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on services areas for the given provider
    
    list: Retrieves the list of service areas for the given provider id (provider_pk)
    
    create:
    Creates a service area for for the given provider.
    The area is a geometrical polygon that can be set using the formats: GeoJSON, WKT EWKT or HEXEWKB.

    retrieve: Retrieves an specific service area from the given provider id (provider_pk)
    delete: Deletes an specific service area from the given provider id (provider_pk)
    partial_update: Allows to update a service area partially in he given provider id (provider_pk)
    update: Allows to update a service area completely in he given provider id (provider_pk)
    """
    serializer_class = ServiceAreaSerializer

    def get_queryset(self):
        return ServiceArea.objects.filter(provider=self.kwargs['provider_pk'])

    def perform_create(self, serializer):
        serializer.save(provider_id=self.kwargs['provider_pk'])


@cache_page(60 * 5)
@api_view(['GET'])
def search_service_areas(request):
    """
    Search endpoint for the service areas than contains a geometrical point (lat,lon).
    The geometrical point must be added to the request as a queryparam named location with the form (lat,lon)
    
    (e.g service-areas?location=100,32.2)
    """
    location = request.query_params.get('location')
    if location:
        try:
            # Checking the lat,lon to see if they are correct (if they can be converted to a float)
            lat, lon = map(float, location.split(','))
        except ValueError:
            logger.debug('A bad formatted location pair was received with values: {location}')
            return Response({'message': 'The provided location was bad formatted. Location must be a lat,lon pair'},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            # Making the contains query to the service area converting the lat and lon to a point.
            point = Point(lat, lon)
            service_areas = ServiceArea.objects.filter(area__contains=point)
            serializer = ServiceAreaSerializer(service_areas, many=True)
            return Response(serializer.data)

    else:
        logger.debug('The search endpoint was query without the location endpoint')
        return Response(
            {'message': 'The search endpoint requires a location query param in the form of a lat,lon pair'},
            status=status.HTTP_400_BAD_REQUEST)
