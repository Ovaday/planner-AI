from django.contrib import admin
from telegram.models import Chat, ChatAdmin

# Register your models here.
admin.site.register(Chat, ChatAdmin)