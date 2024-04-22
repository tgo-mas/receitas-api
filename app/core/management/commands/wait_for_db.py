"""
Comando para o Django esperar o Banco de Dados inicializar
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Comando para o Django esperar o banco de dados.
    """

    def handle(self, *args, **options):
        pass
