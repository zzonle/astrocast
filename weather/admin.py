from django.contrib import admin
from .models import Location, WeatherCondition, WeatherQuery


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'city', 'country', 'latitude', 'longitude')
    search_fields = ('name', 'city', 'country', 'user__username')


admin.site.register(WeatherCondition)


@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'latitude', 'longitude', 'target_date', 'created_at')
    list_filter = ('target_date', 'created_at')
    search_fields = ('user__username',)
