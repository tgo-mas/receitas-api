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
