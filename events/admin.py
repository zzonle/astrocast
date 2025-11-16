from django.contrib import admin
from .models import EventRequest, ForecastResult, Report, DataSource

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location', 'target_date', 'activity', 'status', 'created_at')
    list_filter = ('status', 'target_date')
    search_fields = ('activity', 'user__username', 'location__name')

@admin.register(ForecastResult)
class ForecastResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_request', 'label', 'rain_probability', 'adverse_probability', 'created_at')
    list_filter = ('label',)

admin.site.register(Report)
admin.site.register(DataSource)
