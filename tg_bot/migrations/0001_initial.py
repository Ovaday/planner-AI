# Generated by Django 4.1.3 on 2023-03-09 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chat_id", models.CharField(max_length=300)),
                ("counter", models.IntegerField()),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "admin"),
                            ("parents", "parents"),
                            ("user", "user"),
                            ("none", "none"),
                        ],
                        default="none",
                        max_length=10,
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[("russian", "russian"), ("english", "english")],
                        default="english",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]