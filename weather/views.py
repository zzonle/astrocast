from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .serializers import ForecastRequestSerializer, LocationSerializer
from .services import get_weather, WeatherServiceError
from .models import WeatherQuery, Location

class WeatherForecastView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ForecastRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1. Extraemos lat/lon de la validación
        # (Asumiendo que tu serializer devuelve "location": "lat,lon")
        try:
            # Si tu serializer ya devuelve 'latitude' en validated_data, usa eso.
            # Si devuelve el string "lat,lon", lo separamos aquí:
            if 'latitude' in serializer.validated_data:
                lat = serializer.validated_data['latitude']
                lon = serializer.validated_data['longitude']
            else:
                # Fallback para string "lat,lon"
                lat_str, lon_str = serializer.validated_data["location"].split(',')
                lat = float(lat_str)
                lon = float(lon_str)
        except (ValueError, KeyError):
            return Response({"detail": "Error procesando latitud/longitud"}, status=400)

        # 2. Llamada al servicio
        try:
            # Preparamos los datos para get_weather
            service_data = {
                "latitude": lat,
                "longitude": lon,
                "targetDate": serializer.validated_data.get("targetDate") or serializer.validated_data.get("date"),
                "time": serializer.validated_data.get("time")
            }
            data_limpia = get_weather(service_data)
        except WeatherServiceError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # 3. Guardar la consulta en la DB
        query = WeatherQuery.objects.create(
            user=request.user,
            latitude=lat,
            longitude=lon,
            target_date=service_data["targetDate"],
            time=service_data.get("time"),
            raw_request=request.data,
            raw_response=data_limpia,
        )

        # 4. Preparamos la respuesta con el ID extra
        response_data = data_limpia.copy()
        response_data['weather_query_id'] = query.id 

        return Response(response_data, status=status.HTTP_200_OK)


# 🔴 AQUÍ ESTABA EL ERROR: Estas clases deben estar FUERA de WeatherForecastView
# (Sin indentación al inicio)

class LocationListCreateView(generics.ListCreateAPIView):
    """Listar y crear ubicaciones del usuario autenticado."""
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo devolver las ubicaciones del usuario actual
        return Location.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        # Asociar la ubicación al usuario autenticado
        serializer.save(user=self.request.user)


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Recuperar, actualizar o eliminar una ubicación propia."""
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo permitir acciones sobre las ubicaciones del usuario
        return Location.objects.filter(user=self.request.user)