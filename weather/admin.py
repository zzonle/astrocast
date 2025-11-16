from django.contrib import admin
from .models import Location, WeatherCondition

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'city', 'country', 'latitude', 'longitude')
    search_fields = ('name', 'city', 'country', 'user__username')

admin.site.register(WeatherCondition)
