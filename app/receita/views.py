"""
Views para a API de Receitas
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Receita
from receita import serializers


class ReceitaViewSet(viewsets.ModelViewSet):
    """View para API de Receitas."""
    serializer_class = serializers.DetalhesReceitaSerializer
    queryset = Receita.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna receitas criadas pelo user autenticado."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Retorna a classe serializer da requisição."""
        if self.action == 'list':
            return serializers.ReceitaSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Cria uma nova receita."""
        serializer.save(user=self.request.user)