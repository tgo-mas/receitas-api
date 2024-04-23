"""
Testes para a API de usuários
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Cria e retorna um novo usuário"""
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    """Testa os requisitos públicos de usuário"""

    def setUp(self):
        self.client = APIClient()

    def test_criar_user_sucesso(self):
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

    def test_senha_muito_curta(self):
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

    def test_criar_token_user(self):
        """Testa a criação de token de usuário"""
        user_details = {
            'email': 'user@example.com',
            'password': 'exteste123',
            'name': 'Conta Teste',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_criar_token_cred_invalidas(self):
        """Testa requisitar um token com credenciais inválidas"""
        user_details = {
            'email': 'user@example.com',
            'password': 'goodpass'
        }
        create_user(**user_details)

        payload = {
            'email': 'user@example.com',
            'password': 'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_token_sem_senha(self):
        """Testa criação de token sem senha"""
        payload = {
            'email': 'user@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
