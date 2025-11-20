from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import ForecastRequestSerializer
from .services import get_weather, WeatherServiceError


class WeatherForecastView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ForecastRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_limpia = get_weather(serializer.validated_data)
        except WeatherServiceError as e:
            # Error controlado de nuestro servicio
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(data_limpia, status=status.HTTP_200_OK)
