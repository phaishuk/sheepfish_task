from rest_framework import viewsets

from check_handling_service.models import Printer, Check
from check_handling_service.serializers import PrinterSerializer, CheckCreateSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckCreateSerializer
