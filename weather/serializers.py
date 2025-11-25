from rest_framework import serializers


class ForecastRequestSerializer(serializers.Serializer):
    location = serializers.CharField()
    date = serializers.DateField()
    time = serializers.TimeField(
        required=False,
        allow_null=True,
        help_text="Hora opcional, formato HH:MM (por ahora no se usa en el modelo analítico)"
    )

    def validate_location(self, value: str):
        """
        Valida SOLO el formato de location. 
        Debe devolver un string válido, no un dict.
        """
        try:
            lat_str, lon_str = value.split(",")
            float(lat_str.strip())
            float(lon_str.strip())
        except Exception:
            raise serializers.ValidationError(
                "Formato de ubicación inválido. Usa 'lat,lon' (ej: -33.45,-70.67)."
            )

        # devolvemos el string original (ya validado)
        return value

    def validate(self, attrs):
        """
        Transformamos los datos a la estructura que necesita el servicio.
        Aquí ya sabemos que location pasó validate_location.
        """
        loc = attrs["location"]
        lat_str, lon_str = loc.split(",")

        latitude = float(lat_str.strip())
        longitude = float(lon_str.strip())

        # construimos el dict interno que quieres usar en get_weather
        return {
            "latitude": latitude,
            "longitude": longitude,
            "targetDate": attrs["date"],
            "time": attrs.get("time"),
        }


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Location

        model = Location
        fields = ("id", "name", "city", "country", "latitude", "longitude", "created_at")
        read_only_fields = ("id", "created_at")
