"""
Testes para a API de Receitas
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Receita

from receita.serializers import ReceitaSerializer


RECEITAS_URL = reverse('receita:receita-list')


def create_receita(user, **params):
    """Cria e retorna uma receita teste"""
    defaults = {
        'nome': 'Teste de receita',
        'tempo_preparo': 23,
        'preco': Decimal('25.0'),
        'descricao': 'Simples descrição de receita teste.',
        'link': 'https://example.recipe.com'
    }
    defaults.update(params)

    receita = Receita.objects.create(user=user, **defaults)
    return receita


class PublicReceitaTestes(TestCase):
    """Testa as funcionalidades da API de Receitas sem autenticação."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Testa se a autenticação é obrigatória."""
        res = self.client.get(RECEITAS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReceitaTestes(TestCase):
    """Testa funcionalidades de Receita com autenticação."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='senhateste123',
            name='Conta Teste'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_receitas(self):
        """Testa a requisição de várias receitas"""
        create_receita(user=self.user)
        create_receita(user=self.user)

        res = self.client.get(RECEITAS_URL)

        receitas = Receita.objects.all().order_by('-id')
        serializer = ReceitaSerializer(receitas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_receitas_user_auth(self):
        """Testa a requisição de receitas apenas do usuário cadastrado."""
        outro_user = get_user_model().objects.create(
            email='outro@test.com',
            password='outrasenha321'
        )
        create_receita(user=outro_user)
        create_receita(user=outro_user)

        res = self.client.get(RECEITAS_URL)

        receitas = Receita.objects.filter(user=self.user)
        serializer = ReceitaSerializer(receitas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
