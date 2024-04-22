"""
Comando para o Django esperar o Banco de Dados inicializar
"""
from time import sleep

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """
    Comando para o Django esperar o banco de dados.
    """

    def handle(self, *args, **options):
        """Ponto de entrada para o comando"""
        self.stdout.write("Esperando o banco de dados...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Banco de dados iniciando, esperando 1 seg")
                sleep(1)

        self.stdout.write(self.style.SUCCESS("Banco de dados iniciado!"))
