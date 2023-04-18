import os

from django.core.management.base import BaseCommand
from helpers.resourcesPacker import pack_resources

class Command(BaseCommand):
    help = 'Encrypts all resources.'

    def handle(self, *args, **options):
        pack_resources()
