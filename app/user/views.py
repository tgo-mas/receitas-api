"""
Views para a API de Usuários
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    TokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Cria um novo usuário no sistema."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Cria um novo token para o usuário"""
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
