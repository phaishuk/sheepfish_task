import base64
import json
from django.utils import timezone

import requests
from celery import shared_task
from django.template.loader import render_to_string
from django.core import serializers


@shared_task
def convertation_html_to_pdf(check_data: str) -> None:
    check_instance = next(
        serializers.deserialize("json", check_data, ignorenonexistent=True)
    ).object

    check_type_context = (
        "Kлієнтський" if check_instance.type == "client" else "Кухонний"
    )

    context = {
        "order_number": check_instance.order["order_number"],
        "point_id": check_instance.order["point_id"],
        "items": check_instance.order["items"],
        "total_price": sum(
            item["quantity"] * item["price"] for item in check_instance.order["items"]
        ),
        "order_datetime": timezone.now(),
        "check_type": check_type_context,
    }

    html_page = render_to_string("check_template.html", context)

    url = "http://localhost:3000/"

    data = {
        "contents": base64.b64encode(html_page.encode()).decode("utf-8"),
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    path = f"pdf/{check_instance.order['order_number']}_{check_instance.type}.pdf"
    media_prefix = "media/"

    with open(media_prefix + path, "wb") as f:
        f.write(response.content)

    check_instance.status, check_instance.pdf_file = "rendered", path
    check_instance.save()
