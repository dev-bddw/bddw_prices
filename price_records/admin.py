from django.contrib import admin

from .models import (
    FormulaPriceListPriceRecord,
    FormulaPriceRecord,
    PriceListPriceRecord,
    PriceRecord,
)


class PriceRecordAdmin(admin.ModelAdmin):
    pass


class FormulaPriceRecordAdmin(admin.ModelAdmin):
    pass


class PriceListPriceRecordAdmin(admin.ModelAdmin):
    pass


class FormulaPriceListPriceRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(PriceRecord, PriceRecordAdmin)
admin.site.register(FormulaPriceRecord, FormulaPriceRecordAdmin)
admin.site.register(PriceListPriceRecord, PriceListPriceRecordAdmin)
admin.site.register(FormulaPriceListPriceRecord, FormulaPriceListPriceRecordAdmin)
