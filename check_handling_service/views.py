import os

from django.http import HttpResponse
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from check_handling_service.models import Printer, Check
from check_handling_service.serializers import (
    PrinterSerializer,
    CheckCreateSerializer,
    CheckSerializer,
)


class PrinterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

    @action(detail=False, methods=["GET"])
    def rendered_checks(self, request):
        api_key = request.query_params.get("api_key", None)
        if not api_key:
            return Response({"error": "api_key parameter is required."}, status=400)

        printer = Printer.objects.filter(api_key=api_key).first()
        if not printer:
            return Response({"error": "Printer not found."}, status=404)

        rendered_checks = printer.checks.filter(status="rendered")
        serializer = CheckSerializer(rendered_checks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def download_check(self, request):
        file_path = request.data.get("file_path", None)
        if not file_path:
            return Response(
                {"error": "file_path parameter is required."},
                status=400,
            )

        try:
            with open(f"{file_path}", "rb") as file:
                response = HttpResponse(file.read(), content_type="application/pdf")
                response[
                    "Content-Disposition"
                ] = f"attachment; filename='{os.path.basename(file_path)}'"
                path_parts = file_path.split("/")
                desired_path = "/".join(path_parts[1:])
                check = Check.objects.get(pdf_file=desired_path)
                check.status = "printed"
                check.save()
                return response
        except FileNotFoundError:
            return Response({"error": "File not found."}, status=404)


class CheckViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Check.objects.all()
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        serializer = CheckCreateSerializer(data=request.data)

        if serializer.is_valid():
            point_id = serializer.validated_data["point_id"]
            serializer.save()
            printers_objects = Printer.objects.filter(point_id=point_id)
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
        if self.action in ("list", "retrieve"):
            return CheckSerializer
