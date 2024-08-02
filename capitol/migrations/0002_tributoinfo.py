# Generated by Django 5.0.7 on 2024-08-02 01:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("capitol", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TributoInfo",
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
                ("numero_tributo", models.CharField(max_length=20, unique=True)),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("alumno", "Alumno de Unidad Académica"),
                            ("externo", "Persona Externa"),
                        ],
                        default="externo",
                        max_length=10,
                    ),
                ),
                (
                    "unidad_academica",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("distrito", models.IntegerField()),
                ("edad", models.IntegerField()),
                ("habilidades", models.TextField()),
                ("fuerza", models.IntegerField()),
                (
                    "personaje",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]