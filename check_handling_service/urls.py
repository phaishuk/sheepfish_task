from django.urls import path, include
from rest_framework import routers

from check_handling_service.views import CheckViewSet, PrinterViewSet

router = routers.DefaultRouter()
router.register("printer", PrinterViewSet, basename="printer")
router.register("check", CheckViewSet, basename="check")


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "check_handling_service"
