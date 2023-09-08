# Generated by Django 4.2.4 on 2023-09-08 07:11

from django.db import migrations
from django.core.management import call_command


def load_func(apps, schema_editor):
    call_command("loaddata", "data.json")


def to_unload_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "check_handling_service",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.RunPython(load_func, to_unload_func),
    ]