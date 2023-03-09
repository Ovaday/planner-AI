from django.contrib import admin
from tg_bot.models import Chat, ChatAdmin

# Register your models here.
admin.site.register(Chat, ChatAdmin)