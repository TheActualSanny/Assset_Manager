from time import sleep
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    def handle(self, *args, **options):
        db_on = False
        while not db_on:
            try:
                connections['default'].cursor()
                db_on = True
            except:
                self.stdout.write('The database is not on yet! waiting...')
                sleep(2)
        self.stdout.write('Database is set up! running the migrations...')