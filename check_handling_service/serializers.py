from rest_framework import serializers

from check_handling_service.models import Check, Printer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "name", "api_key", "check_type", "point_id")


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ("id", "printer_id", "type", "order", "status", "pdf_file")


class CheckCreateSerializer(serializers.Serializer):
    order_number = serializers.IntegerField()
    point_id = serializers.IntegerField()
    items = serializers.ListField(child=serializers.DictField())

    def validate_order_number(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError(
                "Order number must contain only letters and digits."
            )
        return value

    def validate(self, data):
        point_id = data["point_id"]
        if not Printer.objects.filter(point_id=point_id).exists():
            raise serializers.ValidationError("No printers available for this point.")

        order_number = data["order_number"]
        if Check.objects.filter(order__order_number=order_number).exists():
            raise serializers.ValidationError(
                "Order with this order number already exists."
            )

        items = data["items"]
        if not items:
            raise serializers.ValidationError(
                "At least one item (dish, snack, or beverage) is required."
            )
        return data

    def create(self, validated_data):
        order_number = validated_data.get("order_number")
        point_id = validated_data.get("point_id")
        items = validated_data.get("items", [])

        printers = Printer.objects.filter(point_id=point_id)

        created_checks = []
        for printer in printers:
            order = {
                "order_number": order_number,
                "point_id": point_id,
                "items": items,
            }

            check = Check(
                printer_id=printer,
                type=printer.check_type,
                order=order,
                status="new",
                pdf_file=None,
            )
            check.save()
            created_checks.append(check)

        return created_checks
