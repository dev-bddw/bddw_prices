from django.contrib import admin

from .models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)


class PriceRecordAdmin(admin.ModelAdmin):
    list_display = [
        "cat_series_item",
        "rule_type",
        "rule_display_1",
        "list_price",
        "net_price",
    ]
    search_fields = ["cat_series_item__name", "rule_type", "rule_display_1"]
    list_filter = ["rule_type"]
    ordering = ["order", "rule_display_1"]


class FormulaPriceRecordAdmin(admin.ModelAdmin):

    list_display = [
        "cat_series_item",
        "rule_type",
        "rule_display_1",
        "list_price",
        "net_price",
    ]
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class PriceListPriceRecordAdmin(admin.ModelAdmin):
    list_display = ("cat_series_item", "rule_type", "rule_display_1", "list_price")
    search_fields = ("cat_series_item__name", "rule_display_1")
    list_filter = ("rule_type", "is_surcharge")
    ordering = ("order",)


class FormulaPriceListPriceRecordAdmin(admin.ModelAdmin):
    list_display = ("cat_series_item", "rule_type", "rule_display_1", "list_price")
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


admin.site.register(PriceRecord, PriceRecordAdmin)
admin.site.register(FormulaPriceRecord, FormulaPriceRecordAdmin)
admin.site.register(PriceListPriceRecord, PriceListPriceRecordAdmin)
admin.site.register(FormulaPriceListPriceRecord, FormulaPriceListPriceRecordAdmin)
