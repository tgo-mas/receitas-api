"""
Testes para os models do projeto.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTeste(TestCase):
    """Testa os models"""

    def test_create_user_with_email_success(self):
        """Testa o caso de sucesso para user criado com email."""
        email = "test@example.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
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
