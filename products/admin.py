from django.contrib import admin
from django.db import models
from django.forms import ModelForm

from .models import Category, CatSeriesItem, Item, Series


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 10000
    ordering = ["name"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all().order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SeriesAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 10000
    ordering = ["name"]
    list_display = ["name", "tearsheet_grouping"]
    list_editable = ["tearsheet_grouping"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "series":
            kwargs["queryset"] = Series.objects.all().order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_per_page = 10000
    ordering = ["name"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "item":
            kwargs["queryset"] = Item.objects.all().order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CatSeriesItemAdmin(admin.ModelAdmin):
    search_fields = ["series__name", "category__name", "item__name"]
    list_per_page = 10000
    ordering = ["category__name", "series__name", "item__name"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all().order_by("name")
        elif db_field.name == "series":
            kwargs["queryset"] = Series.objects.all().order_by("name")
        elif db_field.name == "item":
            kwargs["queryset"] = Item.objects.all().order_by("name")
        elif db_field.name == "tear_sheet":
            from tear_sheets.models import TearSheet

            kwargs["queryset"] = TearSheet.objects.all().order_by("title")
        elif db_field.name == "formula_tear_sheet":
            from formula_tear_sheets.models import FormulaTearSheet

            kwargs["queryset"] = FormulaTearSheet.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(CatSeriesItem, CatSeriesItemAdmin)