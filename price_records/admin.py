from django.contrib import admin

from .models import FormulaPriceRecord, PriceRecord


class PriceRecordAdmin(admin.ModelAdmin):
    pass


class FormulaPriceRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(PriceRecord, PriceRecordAdmin)
admin.site.register(FormulaPriceRecord, FormulaPriceRecordAdmin)
