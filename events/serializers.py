from rest_framework import serializers
from .models import EventRequest
from weather.models import WeatherQuery, Location

class EventRequestSerializer(serializers.ModelSerializer):
    # Campo de solo escritura: Recibe el ID del clima (ej: 502)
    weather_query_id = serializers.PrimaryKeyRelatedField(
        queryset=WeatherQuery.objects.all(),
        source='weather_query',
        write_only=True,
        required=False,
        allow_null=True
    )

    # Campo de solo escritura: Recibe el ID de la ubicación
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='location',
        write_only=True
    )
    
    # Campo de lectura: Muestra el nombre de la ubicación
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = EventRequest
        fields = [
            'id',
            'activity',
            'target_date',
            'target_time',
            'location_id',   # Input
            'location_name', # Output
            'weather_query_id', # Input (el link mágico)
            'status',
            'created_at'
        ]
        read_only_fields = ['user', 'status', 'created_at']

    def create(self, validated_data):
        # Asignar automáticamente el usuario logueado
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)