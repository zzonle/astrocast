from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

# 1. Serializer para el registro (Solo escritura)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # El perfil se crea automático por la señal (signals), así que solo creamos el usuario
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# 2. Serializer para actualizar el Perfil (Lectura y Escritura)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('language', 'temperature_unit', 'avatar', 'subscription_plan', 'subscription_expires')
        read_only_fields = ('subscription_plan', 'subscription_expires')

# 3. Serializer para ver el Usuario completo (Lectura - /me)
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')