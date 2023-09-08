# Generated by Django 4.2.4 on 2023-09-08 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Printer",
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
                ("name", models.CharField(max_length=255)),
                ("api_key", models.CharField(max_length=255, unique=True)),
                (
                    "check_type",
                    models.CharField(
                        choices=[("kitchen", "Kitchen"), ("client", "Client")],
                        max_length=7,
                    ),
                ),
                ("point_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Check",
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
                (
                    "type",
                    models.CharField(
                        choices=[("kitchen", "Kitchen"), ("client", "Client")],
                        max_length=7,
                    ),
                ),
                ("order", models.JSONField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("rendered", "Rendered"),
                            ("printed", "Printed"),
                        ],
                        max_length=8,
                    ),
                ),
                ("pdf_file", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "printer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checks",
                        to="check_handling_service.printer",
                    ),
                ),
            ],
        ),
    ]
