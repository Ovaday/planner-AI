from django.db import models
from django.contrib import admin

class Chat(models.Model):
    chat_id = models.CharField(max_length=300)
    counter = models.IntegerField()

class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'counter']