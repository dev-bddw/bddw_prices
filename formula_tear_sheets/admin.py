from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin

from .models import (
    FormulaImageCaption,
    FormulaTearSheet,
    FormulaTearSheetDetail,
    FormulaTearSheetFooterDetail,
)


class FormulaTearsheetAdmin(admin.ModelAdmin):
    search_fields = [
        "title",
        "catseriesitem__category__name",
        "catseriesitem__series__name",
        "catseriesitem__item__name",
    ]
    list_per_page = 10000
    ordering = ["title"]
    list_display = ["title", "template", "updated_on"]


class FormulaTearsheetDetailAdmin(admin.ModelAdmin):
    search_fields = [
        "tear_sheet__title",
        "name",
        "details",
    ]
    list_per_page = 10000
    ordering = ["tear_sheet__title", "order"]
    list_display = ["tear_sheet", "name", "order"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tear_sheet":
            kwargs["queryset"] = FormulaTearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormulaImageCaptionAdmin(admin.ModelAdmin):
    search_fields = [
        "tear_sheet__title",
        "caption_title",
        "caption",
    ]
    list_per_page = 10000
    ordering = ["tear_sheet__title", "order_no"]
    list_display = ["tear_sheet", "caption_title", "order_no"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tear_sheet":
            kwargs["queryset"] = FormulaTearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FormulaTearSheetFooterDetailAdmin(admin.ModelAdmin):
    search_fields = [
        "tear_sheet__title",
        "name",
        "details",
    ]
    list_per_page = 10000
    ordering = ["tear_sheet__title", "order"]
    list_display = ["tear_sheet", "name", "order"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tear_sheet":
            kwargs["queryset"] = FormulaTearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(FormulaTearSheet, FormulaTearsheetAdmin)
admin.site.register(FormulaTearSheetDetail, FormulaTearsheetDetailAdmin)
admin.site.register(FormulaTearSheetFooterDetail, FormulaTearSheetFooterDetailAdmin)
admin.site.register(FormulaImageCaption, FormulaImageCaptionAdmin)


admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
