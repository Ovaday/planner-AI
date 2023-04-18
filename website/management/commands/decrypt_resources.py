import os

from django.core.management.base import BaseCommand
from helpers.resourcesPacker import unpack_resources

class Command(BaseCommand):
    help = 'Decrypts all resources.'

    def handle(self, *args, **options):
        unpack_resources()
