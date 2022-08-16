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
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class FormulaTearsheetDetailAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class FormulaImageCaptionAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class FormulaTearSheetFooterDetailAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


admin.site.register(FormulaImageCaption, FormulaImageCaptionAdmin)
admin.site.register(FormulaTearSheet, FormulaTearsheetAdmin)
admin.site.register(FormulaTearSheetDetail, FormulaTearsheetDetailAdmin)
admin.site.register(FormulaTearSheetFooterDetail, FormulaTearSheetFooterDetailAdmin)


admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
