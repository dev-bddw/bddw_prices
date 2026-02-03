from django.contrib import admin

from .models import (
    ImageCaption,
    TearSheet,
    TearSheetDetail,
    TearSheetFooterDetail,
    TearSheetFormatting,
)


class TearsheetAdmin(admin.ModelAdmin):
    search_fields = [
        "title",
        "catseriesitem__category__name",
        "catseriesitem__series__name",
        "catseriesitem__item__name",
    ]
    list_per_page = 10000
    ordering = ["title"]
    list_display = ["title", "template", "updated_on"]


class TearsheetDetailAdmin(admin.ModelAdmin):
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
            kwargs["queryset"] = TearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ImageCaptionAdmin(admin.ModelAdmin):
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
            kwargs["queryset"] = TearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TearSheetFooterDetailAdmin(admin.ModelAdmin):
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
            kwargs["queryset"] = TearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TearSheetFormattingAdmin(admin.ModelAdmin):
    list_display = ["tear_sheet", "last_updated"]
    ordering = ["tear_sheet__title", "-last_updated"]
    search_fields = ["tear_sheet__title"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tear_sheet":
            kwargs["queryset"] = TearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(TearSheet, TearsheetAdmin)
admin.site.register(TearSheetDetail, TearsheetDetailAdmin)
admin.site.register(TearSheetFooterDetail, TearSheetFooterDetailAdmin)
admin.site.register(ImageCaption, ImageCaptionAdmin)
admin.site.register(TearSheetFormatting, TearSheetFormattingAdmin)