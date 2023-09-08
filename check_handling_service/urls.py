from django.urls import path, include
from rest_framework import routers

from check_handling_service.views import CheckViewSet, PrinterViewSet

router = routers.DefaultRouter()

router.register("checks", CheckViewSet, basename="check")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "printers/rendered_checks/",
        PrinterViewSet.as_view({"get": "rendered_checks"}),
        name="printer-rendered-checks",
    ),
    path(
        "printers/download_check/",
        PrinterViewSet.as_view({"post": "download_check"}),
        name="printer-download-check",
    ),
]

app_name = "check_handling_service"
