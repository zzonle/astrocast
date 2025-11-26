from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer
from .models import UserProfile

# Vista de Registro (Pública)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# Vista de "Mi Perfil" (Privada)
class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,) # <--- Solo con Token

    def get_object(self):
        # Devuelve el usuario conectado actualmente
        return self.request.user

# Vista para actualizar el Perfil de Usuario (Privada)
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        # Devuelve el perfil del usuario conectado
        return self.request.user.profile