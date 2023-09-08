from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core import serializers
from check_handling_service.models import Check
from tasks import convertation_html_to_pdf


@receiver(post_save, sender=Check)
def create_check(sender, instance, created, **kwargs):
    if created:
        check_data = serializers.serialize("json", [instance])
        convertation_html_to_pdf.delay(check_data=check_data)
