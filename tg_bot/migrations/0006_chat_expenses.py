# Generated by Django 4.1.3 on 2023-04-19 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tg_bot", "0005_alter_chat_last_conversation_alter_chat_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="expenses",
            field=models.FloatField(default=0),
        ),
    ]
