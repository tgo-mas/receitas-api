"""
Testes para a API de usuários
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Cria e retorna um novo usuário"""
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    """Testa os requisitos públicos de usuário"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_sucesso(self):
        """Testa criar um usuário com caso de sucesso"""
        payload = {
            'email': 'test@example.com',
            'password': 'exteste123',
            'name': 'Conta Teste',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_email_ja_existe(self):
        """Testa criar um usuário com caso de erro de email já existente"""
        payload = {
            'email': 'test@example.com',
            'password': 'exteste123',
            'name': 'Conta Teste',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Testa criar um usuário com erro de senha menor que 5 caracteres"""
        payload = {
            'email': 'test@example.com',
            'password': 'ext2',
            'name': 'Conta Teste',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)