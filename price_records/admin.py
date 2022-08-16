from django.contrib import admin

from .models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)


class PriceRecordAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class FormulaPriceRecordAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class PriceListPriceRecordAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class FormulaPriceListPriceRecordAdmin(admin.ModelAdmin):
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
