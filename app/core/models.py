"""
Models para o Banco de Dados
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Administrador de usuários"""

    def create_user(self, email, password=None, **extra_fields):
        """Cria, salva e retorna um novo usuário"""
        if not email:
            raise ValueError("Usuário deve ter um email.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set_password serve para não termos acesso direto à senha do usuário
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Cria e retorna um novo superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Usuário do sistema."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Receita(models.Model):
    """Objeto receita"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    tempo_preparo = models.IntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nome
