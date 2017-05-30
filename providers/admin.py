from django.contrib.gis import admin
from .models import Provider, ServiceArea


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass


admin.site.register(ServiceArea, admin.GeoModelAdmin)
