"""
Views para a API de Usuários
"""
from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Cria um novo usuário no sistema."""
    serializer_class = UserSerializer
