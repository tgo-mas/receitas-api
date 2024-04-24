"""
Serializers para a API de Receitas
"""
from rest_framework import serializers

from core.models import Receita


class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para Receita."""

    class Meta:
        model = Receita
        fields = ['id', 'nome', 'tempo_preparo', 'preco', 'link']
        read_only_fields = ['id']


class DetalhesReceitaSerializer(ReceitaSerializer):
    """Serializer para detalhes de Receita."""

    class Meta(ReceitaSerializer.Meta):
        fields = ReceitaSerializer.Meta.fields + ['descricao']
