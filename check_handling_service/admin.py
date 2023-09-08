from django.contrib import admin
from check_handling_service.models import Printer, Check


class CheckAdmin(admin.ModelAdmin):
    list_display = ("order_number", "point_id", "printer_id", "type", "status")
    list_filter = ("printer_id", "type", "status")
    search_fields = ("printer_id__name",)
    readonly_fields = ("order_number", "point_id")

    def order_number(self, obj):
        return obj.order.get("order_number")

    def point_id(self, obj):
        return obj.order.get("point_id")


class PrinterAdmin(admin.ModelAdmin):
    list_display = ("name", "api_key", "check_type", "point_id")
    search_fields = ("name", "api_key")


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
