from django.conf.urls import include, url
from rest_framework_nested import routers
from . import views

# === REST Routers === #
router = routers.SimpleRouter()
router.register(r'providers', views.ProviderViewSet, base_name='provider')
provider_router = routers.NestedSimpleRouter(router, r'providers', lookup='provider')
provider_router.register(r'service-areas', views.ServiceAreaViewSet, base_name='provider-service-area')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(provider_router.urls)),
    url(r'^service-areas$', view=views.search_service_areas, name='search-service-areas')
]
