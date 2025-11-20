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
        try:
            lat_str, lon_str = value.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
        except Exception:
            raise serializers.ValidationError(
                "Formato de ubicación inválido. Usa 'lat,lon' (ej: -33.45,-70.67)."
            )

        return {"latitude": lat, "longitude": lon}

    def to_internal_value(self, data):
        raw = super().to_internal_value(data)
        location = self.validate_location(raw["location"])

        return {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "targetDate": raw["date"],  
            "time": raw.get("time"),
        }
