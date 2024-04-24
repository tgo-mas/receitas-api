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

from receita.serializers import (
    ReceitaSerializer,
    DetalhesReceitaSerializer,
)


RECEITAS_URL = reverse('receita:receita-list')


def detalhes_url(id_receita):
    """Cria e retorna a URL para a Receita."""
    return reverse('receita:receita-detail', args=[id_receita])


def create_receita(user, **params):
    """Cria e retorna uma receita teste."""
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

def create_user(**params):
    """Cria e retorna um novo usuário."""
    return get_user_model().objects.create(**params)


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
        self.user = create_user(
            email='user@example.com',
            password='senhateste123'
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
        outro_user = create_user(
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

    def test_get_detalhes_receita(self):
        """Testa coletar detalhes de uma receita."""
        receita = create_receita(user=self.user)

        url = detalhes_url(receita.id)
        res = self.client.get(url)
        serializer = DetalhesReceitaSerializer(receita)

        self.assertEqual(res.data, serializer.data)

    def test_criar_receita(self):
        """Testa criar uma receita."""
        payload = {
            'nome': 'Teste de Receita',
            'tempo_preparo': 23,
            'preco': Decimal('5.95'),
            'descricao': 'Descrição simples de receita',
        }
        res = self.client.post(RECEITAS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        receita = Receita.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(receita, k), v)
        self.assertEqual(receita.user, self.user)

    def test_atualizar_parte_receita(self):
        """Testa um update parcial em uma receita."""
        original_link = 'https://example.com/receita.pdf'
        receita = create_receita(
            user=self.user,
            nome='Exemplo de receita',
            link=original_link
        )

        payload = {'nome': 'Teste de receita'}
        url = detalhes_url(receita.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        receita.refresh_from_db()

        self.assertEqual(receita.nome, payload['nome'])
        self.assertEqual(receita.link, original_link)
        self.assertEqual(receita.user, self.user)

    def test_atualizar_receita(self):
        """Teste para atualização total de receita."""
        receita = create_receita(
            user=self.user,
            nome='Exemplo de receita',
            tempo_preparo=30,
            preco=Decimal('5.60'),
            link='https://example.com/receita.pdf',
            descricao='Essa aqui é uma descrição.'
        )

        payload = {
            'nome': 'Nova receita',
            'tempo_preparo': 40,
            'preco': Decimal('6.50'),
            'link': 'https://novolink.com/receita.pdf',
            'descricao': 'Essa aqui é uma descrição',
        }
        url = detalhes_url(receita.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        receita.refresh_from_db()
        
        for k, v in payload.items():
            self.assertEqual(getattr(receita, k), v)
        self.assertEqual(receita.user, self.user)

    def test_erro_atualizar_user(self):
        """Testa se tentar atualizar o user de uma receita retorna erro."""
        novo_user = create_user(email='user2@example.com', password='senhasegundo')
        receita = create_receita(user=self.user)

        payload = {
            'user': novo_user.id
        }
        url = detalhes_url(receita.id)
        self.client.patch(url, payload)
        receita.refresh_from_db()

        self.assertEqual(receita.user, self.user)
    
    def test_excluir_receita(self):
        """Testa a exclusão de receitas."""
        receita = create_receita(user=self.user)

        url = detalhes_url(receita.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Receita.objects.filter(id=receita.id).exists())

    def test_erro_excluir_receitas_de_outros(self):
        """Testa tentar ver receitas de outros usuários (erro)"""
        novo_user = create_user(email='novouser@example.com', password='senhanovo')
        receita = create_receita(user=novo_user)

        url = detalhes_url(receita.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Receita.objects.filter(id=receita.id).exists())
