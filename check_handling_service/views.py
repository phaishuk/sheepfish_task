from rest_framework import viewsets, status
from rest_framework.response import Response

from check_handling_service.models import Printer, Check
from check_handling_service.serializers import (
    PrinterSerializer,
    CheckCreateSerializer,
    CheckSerializer,
)


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CheckCreateSerializer(data=request.data)

        if serializer.is_valid():
            point_id = serializer.validated_data["point_id"]
            printers_objects = Printer.objects.filter(point_id=point_id)
            serializer.save()
            return Response(
                {
                    "message": f"Created {len(printers_objects)} check(s) for point number {point_id}"
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "create":
            return CheckCreateSerializer
        if self.action in ("list", "retrieve", "update", "partial_update", "delete"):
            return CheckSerializer
