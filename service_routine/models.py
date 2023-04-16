from django.db import models
from django.contrib import admin

class ServiceM(models.Model):
    chat = models.ForeignKey('tg_bot.Chat', on_delete=models.CASCADE)
    schedule = models.ForeignKey('django_q.Schedule', on_delete=models.CASCADE)
    request = models.TextField()


class ServiceMAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'schedule', 'request']