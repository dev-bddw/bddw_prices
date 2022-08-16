from django.contrib import admin

from .models import ImageCaption, TearSheet, TearSheetDetail, TearSheetFooterDetail


class TearsheetAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class TearsheetDetailAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class ImageCaptionAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


class TearSheetFooterDetailAdmin(admin.ModelAdmin):
    search_fields = [
        "cat_series_item__category__name",
        "cat_series_item__series__name",
        "cat_series_item__item__name",
    ]
    list_per_page = 10000


admin.site.register(ImageCaption, ImageCaptionAdmin)
admin.site.register(TearSheet, TearsheetAdmin)
admin.site.register(TearSheetDetail, TearsheetDetailAdmin)
admin.site.register(TearSheetFooterDetail, TearSheetFooterDetailAdmin)
