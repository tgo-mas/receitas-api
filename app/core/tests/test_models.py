"""
Testes para os models do projeto.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTeste(TestCase):
    """Testa os models"""

    def test_criar_user_com_email_sucesso(self):
        """Testa o caso de sucesso para user criado com email."""
        email = "test@example.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalizado(self):
        """Testa a normalização de email para novos usuários"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_user_sem_email(self):
        """Testa a criação de usuário sem email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_criar_superuser(self):
        """Testa a criação de superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
