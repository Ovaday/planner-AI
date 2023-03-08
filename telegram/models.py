from django.db import models

class Chat(models.Model):
    chat_id = models.CharField(max_length=300)
    counter = models.IntegerField()