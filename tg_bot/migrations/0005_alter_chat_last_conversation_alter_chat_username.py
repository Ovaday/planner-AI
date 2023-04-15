# Generated by Django 4.1.3 on 2023-03-12 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tg_bot", "0004_chat_current_mode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="last_conversation",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="chat",
            name="username",
            field=models.CharField(blank=True, default="", max_length=300, null=True),
        ),
    ]