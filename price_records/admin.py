from django.contrib import admin

from .models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
    TearSheetPriceRecord,
)


class PriceRecordAdmin(admin.ModelAdmin):
    list_display = [
        "bin_id",
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
        "rule_type",
        "rule_display_1",
    ]
    list_filter = ["rule_type"]
    ordering = ["cat_series_item__category__name", "rule_display_1"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cat_series_item":
            from products.models import CatSeriesItem

            kwargs["queryset"] = CatSeriesItem.objects.all().order_by(
                "category__name", "series__name", "item__name"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    ordering = ["cat_series_item__category__name", "rule_display_1"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cat_series_item":
            from products.models import CatSeriesItem

            kwargs["queryset"] = CatSeriesItem.objects.all().order_by(
                "category__name", "series__name", "item__name"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PriceListPriceRecordAdmin(admin.ModelAdmin):
    list_display = ("cat_series_item", "rule_type", "rule_display_1", "list_price")
    search_fields = ("cat_series_item__category__name", "rule_display_1")
    list_filter = ("rule_type", "is_surcharge")
    ordering = ("cat_series_item__category__name", "rule_display_1")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cat_series_item":
            from products.models import CatSeriesItem

            kwargs["queryset"] = CatSeriesItem.objects.all().order_by(
                "category__name", "series__name", "item__name"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormulaPriceListPriceRecordAdmin(admin.ModelAdmin):
    list_display = ("cat_series_item", "rule_type", "rule_display_1", "list_price")
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000
    ordering = ["cat_series_item__category__name", "rule_display_1"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cat_series_item":
            from products.models import CatSeriesItem

            kwargs["queryset"] = CatSeriesItem.objects.all().order_by(
                "category__name", "series__name", "item__name"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TearSheetPriceRecordAdmin(admin.ModelAdmin):
    list_display = ["tear_sheet", "price_record", "formula_price_record", "display_order", "is_active"]
    list_filter = ["is_active", "tear_sheet"]
    ordering = ["tear_sheet__title", "display_order"]
    search_fields = ["tear_sheet__title"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tear_sheet":
            from tear_sheets.models import TearSheet

            kwargs["queryset"] = TearSheet.objects.all().order_by("title")
        elif db_field.name == "price_record":
            kwargs["queryset"] = PriceRecord.objects.all().order_by(
                "cat_series_item__category__name", "rule_display_1"
            )
        elif db_field.name == "formula_price_record":
            kwargs["queryset"] = FormulaPriceRecord.objects.all().order_by(
                "cat_series_item__category__name", "rule_display_1"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(PriceRecord, PriceRecordAdmin)
admin.site.register(FormulaPriceRecord, FormulaPriceRecordAdmin)
admin.site.register(PriceListPriceRecord, PriceListPriceRecordAdmin)
admin.site.register(FormulaPriceListPriceRecord, FormulaPriceListPriceRecordAdmin)
admin.site.register(TearSheetPriceRecord, TearSheetPriceRecordAdmin)