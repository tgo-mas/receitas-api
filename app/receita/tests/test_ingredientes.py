"""
Testa as funcionalidades da API de ingredientes.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingrediente,
    Receita
)

from receita.serializers import IngredienteSerializer


INGREDIENTES_URL = reverse('receita:ingrediente-list')


def detalhes_url(id):
    """Retorna a url para detalhes de um ingrediente."""
    return reverse('receita:ingrediente-detail', args=[id])


def create_user(email='test@example.com', password='senhateste'):
    """Cria e retorna um novo usuário para testes."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredienteTestes(TestCase):
    """Testes publicos para Ingredientes."""

    def setUp(self):
        self.client = APIClient()

    def test_listar_ingredientes_publico(self):
        """Testa se a autenticação é obrigatória para listar ingredientes."""
        res = self.client.get(INGREDIENTES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredienteTestes(TestCase):
    """Testes para ingredientes com usuário logado."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_listar_ingredientes(self):
        """Testa a listagem de ingredientes."""
        Ingrediente.objects.create(
            user=self.user,
            nome='Abacaxi'
        )
        Ingrediente.objects.create(
            user=self.user,
            nome='Maçã'
        )

        res = self.client.get(INGREDIENTES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredientes = Ingrediente.objects.all().order_by('-nome')
        serializer = IngredienteSerializer(ingredientes, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_ingredientes_privados(self):
        """Testa se os ingredientes de outro usuário são ocultados."""
        outro_user = create_user(
            email='outro@example.com',
            password='outrasenha'
        )
        Ingrediente.objects.create(
            user=outro_user,
            nome='Carne bovina'
        )
        ing = Ingrediente.objects.create(
            user=self.user,
            nome='Carne de porco'
        )

        res = self.client.get(INGREDIENTES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nome'], ing.nome)
        self.assertEqual(res.data[0]['id'], ing.id)

    def test_atualizar_ingrediente(self):
        """Testa a atualização de ingrediente."""
        ing = Ingrediente.objects.create(user=self.user, nome='Banana')

        payload = {'nome': 'Limão'}
        res = self.client.put(detalhes_url(ing.id), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ing.refresh_from_db()
        self.assertEqual(ing.nome, payload['nome'])

    def test_excluir_ingrediente(self):
        """Testa a exclusão de ingredientes."""
        ing = Ingrediente.objects.create(user=self.user, nome='Abacaxi')

        res = self.client.delete(detalhes_url(ing.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ings = Ingrediente.objects.filter(user=self.user)
        self.assertFalse(ings.exists())

    def test_filtrar_ingrediente_por_receita(self):
        '''Testa a filtragem de ingredientes associados a receitas.'''
        ing1 = Ingrediente.objects.create(user=self.user, nome='Farinha de trigo')
        ing2 = Ingrediente.objects.create(user=self.user, nome='Queijo')

        receita = Receita.objects.create(
            user=self.user,
            nome='Pizza',
            tempo_preparo=40,
            preco=50.0)
        receita.ingredientes.add(ing1)

        res = self.client.get(INGREDIENTES_URL, {'assigned_only': 1})

        s1 = IngredienteSerializer(ing1)
        s2 = IngredienteSerializer(ing2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtro_ingredientes_unique(self):
        '''Testa se o filtro de ingredientes não retorna ingredientes repetidos.'''
        ing = Ingrediente.objects.create(user=self.user, nome='Ovo')
        Ingrediente.objects.create(user=self.user, nome='Lentilha')

        r1 = Receita.objects.create(
            user=self.user,
            nome='Ovo frito',
            tempo_preparo=5,
            preco=5.0)
        r2 = Receita.objects.create(
            user=self.user,
            nome='Ovo mexido',
            tempo_preparo=7,
            preco=7.0)
        r1.ingredientes.add(ing)
        r2.ingredientes.add(ing)

        res = self.client.get(INGREDIENTES_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)

