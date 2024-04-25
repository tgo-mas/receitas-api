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

    def _get_or_create_categorias(self, categorias, receita):
        """Recupera ou cria categorias."""
        auth_user = self.context['request'].user
        for categoria in categorias:
            cat_obj, created = Categoria.objects.get_or_create(
                user=auth_user,
                **categoria
            )
            receita.categorias.add(cat_obj)

    def create(self, validated_data):
        """Cria uma nova receita."""
        categorias = validated_data.pop('categorias', [])
        receita = Receita.objects.create(**validated_data)
        self._get_or_create_categorias(categorias, receita)

        return receita

    def update(self, instance, validated_data):
        """Atualiza uma receita."""
        categorias = validated_data.pop('categorias', None)
        if categorias is not None:
            instance.categorias.clear()
            self._get_or_create_categorias(categorias, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class DetalhesReceitaSerializer(ReceitaSerializer):
    """Serializer para detalhes de Receita."""

    class Meta(ReceitaSerializer.Meta):
        fields = ReceitaSerializer.Meta.fields + ['descricao']
