from django.conf.urls import include
from rest_framework import routers
from . import views

# === REST Routers === #
router = routers.SimpleRouter()
router.register(r'', views.ProviderViewSet, base_name='provider')

urlpatterns = router.urls
