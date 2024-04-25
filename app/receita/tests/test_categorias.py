"""
Testa a API de Categorias de receitas.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Categoria

from receita.serializers import CategoriaSerializer


CATEGORIAS_URL = reverse('receita:categoria-list')


def detalhes_url(id):
    """Cria e retorna uma URL para o id de Receita"""
    return reverse('receita:categoria-detail', args=[id])


def create_user(email='test@example.com', password='senhateste123'):
    """Cria e retorna um novo usuário."""
    return get_user_model().objects.create(email=email, password=password)


class PublicCategoriaTestes(TestCase):
    """Testa as funcionalidades de Categoria sem autenticação."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_obrigatorio(self):
        """Testa se a autenticação é necessária para listar categorias."""
        res = self.client.get(CATEGORIAS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriaTestes(TestCase):
    """Testa funcionalidades de Categoria com autenticação."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_listar_categorias(self):
        """Testa a listagem de categorias."""
        Categoria.objects.create(user=self.user, nome='Vegano')
        Categoria.objects.create(user=self.user, nome='Sobremesa')

        res = self.client.get(CATEGORIAS_URL)
        categorias = Categoria.objects.all().order_by('-nome')
        serializer = CategoriaSerializer(categorias, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_categorias_privadas(self):
        """Testa se as categorias listadas são apenas do usuário logado."""
        novo_user = create_user(
            email='novouser@example.com',
            password='novasenha123'
        )
        Categoria.objects.create(user=novo_user, nome='Cítrica')
        categoria = Categoria.objects.create(user=self.user, nome='Guloseima')

        res = self.client.get(CATEGORIAS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nome'], categoria.nome)
        self.assertEqual(res.data[0]['id'], categoria.id)

    def test_atualizar_categoria(self):
        """Testa a atualização de categoria."""
        categoria = Categoria.objects.create(user=self.user, nome='Ceia')

        url = detalhes_url(categoria.id)
        payload = {'nome': 'Lanche da madrugada'}
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        categoria.refresh_from_db()
        self.assertEqual(categoria.nome, payload['nome'])

    def test_exclui_categoria(self):
        """Testa excluir uma categoria."""
        categoria = Categoria.objects.create(user=self.user, nome='Salgado')

        url = detalhes_url(categoria.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        categorias = Categoria.objects.filter(user=self.user)
        self.assertFalse(categorias.exists())
