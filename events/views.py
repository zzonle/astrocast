# events/views.py
from rest_framework import generics, permissions
from .models import EventRequest
from .serializers import EventRequestSerializer

class EventListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista los eventos del usuario.
    POST: Crea un evento nuevo (asociado opcionalmente a un weather_query_id).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventRequestSerializer

    def get_queryset(self):
        # Filtramos por usuario y optimizamos la consulta (join con location)
        return EventRequest.objects.filter(
            user=self.request.user
        ).select_related('location', 'weather_query').order_by('-created_at')