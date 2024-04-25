"""
Serializers para a API de Receitas
"""
from rest_framework import serializers

from core.models import (
    Receita,
    Categoria
)


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para categoria de receitas."""

    class Meta:
        model = Categoria
        fields = ['id', 'nome']
        read_only_fields = ['id']


class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para Receita."""
    categorias = CategoriaSerializer(many=True, required=False)

    class Meta:
        model = Receita
        fields = ['id', 'nome', 'tempo_preparo', 'preco', 'link', 'categorias']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Cria uma nova receita."""
        categorias = validated_data.pop('categorias', [])
        receita = Receita.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for categoria in categorias:
            cat_obj, created = Categoria.objects.get_or_create(
                user=auth_user,
                **categoria
            )
            receita.categorias.add(cat_obj)

        return receita


class DetalhesReceitaSerializer(ReceitaSerializer):
    """Serializer para detalhes de Receita."""

    class Meta(ReceitaSerializer.Meta):
        fields = ReceitaSerializer.Meta.fields + ['descricao']
