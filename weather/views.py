# weather/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import ForecastRequestSerializer
from .services import get_weather, WeatherServiceError
from .models import WeatherQuery


class WeatherForecastView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ForecastRequestSerializer(data=request.data)
        # Esto lanza ValidationError (400) solo si hay errores de validación
        serializer.is_valid(raise_exception=True)

        try:
            data_limpia = get_weather(serializer.validated_data)
        except WeatherServiceError as e:
            # Error controlado de nuestro servicio externo
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # --- Guardar la consulta en la base de datos ---
        WeatherQuery.objects.create(
            user=request.user,  # ya que el endpoint requiere autenticación
            latitude=serializer.validated_data["latitude"],
            longitude=serializer.validated_data["longitude"],
            target_date=serializer.validated_data["targetDate"],
            time=serializer.validated_data.get("time"),
            raw_request=request.data,      # dict que mandó el cliente
            raw_response=data_limpia,      # lo que le devolviste
        )
        # ------------------------------------------------

        return Response(data_limpia, status=status.HTTP_200_OK)
