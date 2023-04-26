from django.db import models
from django.contrib import admin

class Chat(models.Model):
    chat_id = models.CharField(max_length=300)
    counter = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    whisper_tokens = models.FloatField(default=0)
    expenses = models.FloatField(default=0)

    is_approved = models.BooleanField(default=False)
    role = models.CharField(choices=[('admin', 'admin'),
                                     ('parents', 'parents'),
                                     ('user', 'user'),
                                     ('none', 'none'),],
                            default='none',
                            max_length=10)
    language = models.CharField(choices=[('russian', 'russian'),
                                         ('english', 'english'),],
                                default='english',
                                max_length=10)
    last_conversation = models.TextField(default='', null=True, blank=True)
    username = models.CharField(max_length=300, default='', null=True, blank=True)
    current_mode = models.CharField(max_length=300, default='chatGPT')

    def money_used(self):
        return '$ ' + str(self.expenses)


class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'chat_id', 'counter', 'is_approved', 'money_used', "whisper_tokens"]