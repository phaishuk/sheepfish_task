from django.db import models


CHECK_TYPE_CHOICES = [
    ("kitchen", "Kitchen"),
    ("client", "Client"),
]


class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=7, choices=CHECK_TYPE_CHOICES)
    point_id = models.IntegerField()

    def __str__(self):
        return f"{self.check_type} printer {self.name} in {self.point_id}"


class Check(models.Model):
    CHECK_STATUS_CHOICES = [
        ("new", "New"),
        ("rendered", "Rendered"),
        ("printed", "Printed"),
    ]

    printer_id = models.ForeignKey(
        to=Printer, on_delete=models.CASCADE, related_name="checks"
    )
    type = models.CharField(max_length=7, choices=CHECK_TYPE_CHOICES)
    order = models.JSONField()
    status = models.CharField(max_length=8, choices=CHECK_STATUS_CHOICES)
    pdf_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.order.order_number
