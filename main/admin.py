from django.contrib import admin
from .models import Order, SatelliteModel, Photo, BadZoneModel

admin.site.register(Order)
admin.site.register(SatelliteModel)
admin.site.register(Photo)
admin.site.register(BadZoneModel)
